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


if __name__ == "__main__":
    unittest.main()
