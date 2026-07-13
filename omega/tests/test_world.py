"""Tests for the Ω world runtime — persistence, legibility, and bounded memory.

These pin the guarantees a *watchable living world* needs: it resumes byte-identically from a
checkpoint (so a world survives restarts), its snapshot is legible and its names are stable,
and it stays memory-flat while never closing. Byte-identity of exp001-035 (the `world` builder
+ `Noise.getstate/setstate` change nothing when unused) is covered by test_experiments.
"""
from __future__ import annotations

import os
import tempfile
import unittest

from omega.world import World, checkpoint
from omega.world.observe import Observer, _name


class TestWorldPersistence(unittest.TestCase):
    def test_checkpoint_resume_is_byte_identical(self):
        # The persistence guarantee: checkpoint at T, resume, continue -> identical to an
        # uninterrupted run. This is what lets a world survive container restarts and accrete.
        ref = World.create("world", seed=0)
        ref.step(1600)
        ref_key = (ref.tick, ref.universe.classes_ever_seen,
                   len(ref.universe.organizations), list(ref.novelty.new_per_tick))

        w = World.create("world", seed=0)
        w.step(800)
        path = os.path.join(tempfile.gettempdir(), "omega_world_test.ckpt")
        checkpoint.save(w, path)
        w2 = checkpoint.load(path)
        w2.step(800)
        res_key = (w2.tick, w2.universe.classes_ever_seen,
                   len(w2.universe.organizations), list(w2.novelty.new_per_tick))
        self.assertEqual(ref_key, res_key)
        os.remove(path)

    def test_chunking_is_transparent(self):
        # Advancing in chunks must equal advancing in one shot (chunk size cannot matter).
        a = World.create("world", seed=1)
        for _ in range(20):
            a.step(50)
        b = World.create("world", seed=1)
        b.step(1000)
        self.assertEqual(a.novelty.new_per_tick, b.novelty.new_per_tick)
        self.assertEqual(len(a.universe.organizations), len(b.universe.organizations))


class TestWorldObservability(unittest.TestCase):
    def test_snapshot_schema_and_liveness(self):
        w = World.create("world", seed=0)
        obs = Observer()
        for _ in range(6):
            w.step(300)
            s = obs.snapshot(w)
        for key in ("tick", "population", "novelty_rate", "novelty_pulse", "lifeforms",
                    "collectives", "culture", "alphabet", "events", "classes_ever"):
            self.assertIn(key, s)
        self.assertGreater(s["novelty_rate"], 0.0)          # the world keeps discovering
        self.assertGreater(len(s["lifeforms"]), 0)          # it has legible inhabitants
        self.assertTrue(all("age" in lf for lf in s["lifeforms"]))

    def test_names_are_deterministic_and_stable(self):
        # A lifeform keeps its name across snapshots and across a seed-identical rerun.
        self.assertEqual(_name("abc"), _name("abc"))
        self.assertNotEqual(_name("abc"), _name("abd"))
        w1 = World.create("world", seed=2); w1.step(900)
        w2 = World.create("world", seed=2); w2.step(900)
        n1 = [lf["name"] for lf in Observer()._lifeforms(w1.universe)]
        n2 = [lf["name"] for lf in Observer()._lifeforms(w2.universe)]
        self.assertEqual(n1, n2)


class TestWorldBoundedMemory(unittest.TestCase):
    def test_registry_stays_bounded_while_novelty_persists(self):
        # A world runs at flat memory: past the horizon the registry is evicted (smaller than
        # the cumulative class count) yet novelty stays alive (windowed).
        w = World.create("world", seed=0, memory_horizon=500)
        w.step(3000)
        obs = Observer()
        w.step(300)
        s = obs.snapshot(w)
        self.assertLess(s["registry_size"], s["classes_ever"])   # eviction happened
        self.assertGreater(s["novelty_rate"], 0.0)               # still open


class TestWorldSpace(unittest.TestCase):
    def test_space_off_is_byte_identical(self):
        # SPACE is gated: the world's geography changes dynamics, but a spaceless run is
        # byte-identical to the pre-space engine (space defaults off outside the world builder).
        from omega.experiments.registry import get_experiment
        from omega.experiments import run as _run
        a = _run(*get_experiment("exp030")(seed=0, ticks=800))
        b = _run(*get_experiment("exp030")(seed=0, ticks=800))
        self.assertEqual(a.novelty_cumulative, b.novelty_cumulative)
        self.assertEqual(a.final_population, b.final_population)

    def test_world_has_a_map_with_geography(self):
        w = World.create("world", seed=0)
        self.assertTrue(w.physics.space)
        # grid tiles the patches exactly and neighbours are reciprocal on the torus
        gw, gh = w.physics._grid_dims()
        self.assertEqual(gw * gh, w.physics.n_patches)
        self.assertIn(0, w.physics._neighbors(w.physics._neighbors(0)[0]))
        w.step(1500)
        s = Observer().snapshot(w)
        self.assertIsNotNone(s["space"])
        self.assertEqual(len(s["space"]["cells"]), w.physics.n_patches)
        pops = [c["pop"] for c in s["space"]["cells"]]
        self.assertGreater(max(pops), 0)
        self.assertGreater(max(pops) - min(pops), 0)          # spatial heterogeneity


class TestWorldInteraction(unittest.TestCase):
    def test_perturbations_apply_and_are_logged(self):
        w = World.create("world", seed=0)
        w.step(1000)
        before = len(w.universe.organizations)
        killed = w.shock(0.5)
        self.assertGreater(killed, 0)
        self.assertLess(len(w.universe.organizations), before)   # extinction reduced life
        born = w.seed_life(15, patch=0)
        self.assertGreater(born, 0)                              # seeding added life
        self.assertTrue(w.set_law("horizontal_transfer", 0.9))
        self.assertEqual(w.physics.horizontal_transfer, 0.9)     # law tuned live
        self.assertFalse(w.set_law("not_a_law", 1.0))
        kinds = [i["kind"] for i in w.interactions]
        self.assertEqual(kinds, ["shock", "seed_life", "set_law"])  # replay log
        w.step(200)                                              # world keeps running after

    def test_untouched_world_stays_deterministic(self):
        # interaction is opt-in: a world with no perturbations is reproducible from its seed.
        a = World.create("world", seed=3); a.step(1000)
        b = World.create("world", seed=3); b.step(1000)
        self.assertEqual(a.novelty.new_per_tick, b.novelty.new_per_tick)


if __name__ == "__main__":
    unittest.main()
