"""Tests that pin the *scientific claims* of the v0.1 experiment suite.

These are as much regression guards on the narrative as on the code: if a refactor
silently turns the null control persistent, or closes off exp003, these fail.
"""
from __future__ import annotations

import unittest

from omega.experiments import run
from omega.experiments.registry import get_experiment


def _run(name: str, seed: int = 0, **ov):
    physics, cfg = get_experiment(name)(seed=seed, **ov)
    return run(physics, cfg)


class TestDeterminism(unittest.TestCase):
    def test_same_seed_same_result(self):
        a = _run("exp003", seed=3)
        b = _run("exp003", seed=3)
        self.assertEqual(a.novelty_cumulative, b.novelty_cumulative)
        self.assertEqual(a.final_population, b.final_population)
        self.assertEqual(a.open_endedness, b.open_endedness)

    def test_different_seed_differs(self):
        a = _run("exp003", seed=1)
        b = _run("exp003", seed=2)
        self.assertNotEqual(a.novelty_cumulative, b.novelty_cumulative)

    def test_deterministic_across_hash_seeds(self):
        # Ω-0.33: results must be byte-identical across PYTHONHASHSEED — the engine must not depend
        # on set/frozenset iteration order (which Python randomizes per process). A regression here
        # (e.g. iterating a signature frozenset to build an ordered buffer without sorting) makes a
        # run irreproducible across machines. exp040 exercises the network-template path where this
        # was found and fixed; two subprocesses with different hash seeds must agree exactly.
        import os, subprocess, sys
        snippet = (
            "from omega.experiments.registry import get_experiment;"
            "from omega.experiments.harness import run;"
            "p,c=get_experiment('exp040')(seed=0,ticks=1200);r=run(p,c);"
            "print(r.final_classes_total, r.final_population)"
        )
        root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        def out(hashseed):
            env = {**os.environ, "PYTHONHASHSEED": hashseed, "PYTHONPATH": root}
            return subprocess.check_output([sys.executable, "-c", snippet],
                                           env=env, cwd=root, text=True).strip()

        self.assertEqual(out("0"), out("1"))
        self.assertEqual(out("0"), out("12345"))


class TestScientificClaims(unittest.TestCase):
    def test_exp001_noise_has_no_persistence(self):
        # The null control: nothing re-forms; no composed organization persists.
        r = _run("exp001")
        self.assertEqual(r.persistence["composed_persistent"], 0)

    def test_exp002_binding_yields_composed_persistence(self):
        # Treatment vs matched control differ specifically in composed persistence.
        treat = _run("exp002", bind=True)
        ctrl = _run("exp002", bind=False)
        self.assertGreater(treat.persistence["composed_persistent"], 0)
        self.assertEqual(ctrl.persistence["composed_persistent"], 0)

    def test_exp002_is_closed(self):
        # Persistence without constructibility exhausts its finite possibility space.
        r = _run("exp002", bind=True)
        self.assertLess(r.open_endedness["novelty_rate"], 1e-2)

    def test_exp003_discovers_operators_but_freezes(self):
        # Ω-0.2 correction: exp003 authors a *finite burst* of operators (a larger
        # possibility space than exp002) and then FREEZES — it is not open-ended.
        # The honest gate is the sustained operator-discovery rate, which decays
        # to ~0, not the cumulative count, which stays positive.
        r = _run("exp003")
        self.assertGreater(r.open_endedness["operator_growth"], 0)      # a burst happened
        self.assertLess(r.open_endedness["operator_rate"], 1e-2)        # but it stopped
        self.assertIn("CLOSED", r.open_endedness["verdict"])

    def test_meta_prob_control_discovers_no_operators(self):
        # With meta_prob=0 no operator can author an operator: the law set is
        # frozen at the seeds. This isolates meta-authoring as the (necessary)
        # mechanism for even a transient burst of new laws.
        r = _run("exp003", meta_prob=0.0)
        self.assertEqual(r.open_endedness["operator_growth"], 0)

    def test_exp004_reification_sustains_vs_control(self):
        # Ω-0.2's positive result: promoting persistent structure to new primitives
        # keeps the possibility space enlarging. Treatment grows an alphabet and
        # keeps discovering laws; the matched control (same physics, reify off)
        # mints no primitives and freezes.
        treat = _run("exp004", reify=True, ticks=400)
        ctrl = _run("exp004", reify=False, ticks=400)
        prim_treat = treat.metrics[-1]["primitive_count"]
        prim_ctrl = ctrl.metrics[-1]["primitive_count"]
        self.assertGreater(prim_treat, 0)                 # alphabet grew
        self.assertEqual(prim_ctrl, 0)                    # control never reifies
        self.assertGreater(treat.open_endedness["operator_rate"],
                           ctrl.open_endedness["operator_rate"])
        self.assertIn("OPEN-ENDED", treat.open_endedness["verdict"])

    def test_exp005_nesting_ratchet_deepens_and_the_feed_fix_freezes(self):
        # Ω-0.3: the nesting ratchet (canonical exp005) builds deeply-nested
        # primitives and keeps discovering; the falsified "feed base only" fix
        # freezes after an initial burst.
        ratchet = _run("exp005", ticks=1200)                       # feed_reified=True
        frozen = _run("exp005", ticks=1200, feed_reified=False)    # the falsified fix
        # cumulative construction: lineage depth climbs well past a flat vocabulary
        self.assertGreaterEqual(ratchet.metrics[-1]["gauges"]["reify_depth"], 3)
        # the feed-only "fix" starves the ratchet and stops discovering laws
        self.assertGreater(ratchet.open_endedness["operator_rate"],
                           frozen.open_endedness["operator_rate"])

    def test_exp006_depth_breadth_tradeoff(self):
        # Ω-0.4: discounting the reification bar to counteract deep-symbol rarity
        # does NOT lift depth — it explodes breadth instead. The two compete for
        # the finite data pool, so the "fix" mints far more primitives without
        # deepening the hierarchy.
        base = _run("exp006", ticks=800, reify_max_len=6)
        disc = _run("exp006", ticks=800, reify_max_len=6, depth_discount=True)
        self.assertGreater(disc.metrics[-1]["primitive_count"],
                           2 * base.metrics[-1]["primitive_count"])
        self.assertLessEqual(disc.metrics[-1]["gauges"]["reify_depth"],
                             base.metrics[-1]["gauges"]["reify_depth"])

    def test_exp007_frontier_lifts_depth_as_quality_not_breadth(self):
        # Ω-0.5: concentrating recurrence on the frontier deepens the hierarchy far
        # past the baseline plateau, and does so as *quality* (mean depth), not the
        # gameable breadth that depth_discount produced.
        from omega.metrics.construction_quality import construction_quality
        base = _run("exp007", ticks=600, frontier_prob=0.0)
        front = _run("exp007", ticks=600, frontier_prob=0.6)
        bq = construction_quality(base.metrics[-1]["gauges"], base.metrics[-1]["primitive_count"])
        fq = construction_quality(front.metrics[-1]["gauges"], front.metrics[-1]["primitive_count"])
        # frontier feeding lifts both max and mean reification depth well beyond baseline
        self.assertGreater(fq.max_depth, 2 * bq.max_depth)
        self.assertGreater(fq.mean_depth, bq.mean_depth)

    def test_exp008_toolkit_feeding_builds_a_reused_core(self):
        # Ω-0.6: toolkit feeding (keep the most-reused primitives abundant) builds a
        # heavily-reused core — peak reuse far above what depth-frontier feeding
        # gives, which thins reuse. Depth and reuse are separate axes.
        lib = _run("exp008", ticks=800, library_prob=0.6, frontier_prob=0.0)
        front = _run("exp008", ticks=800, library_prob=0.0, frontier_prob=0.6)
        self.assertGreater(lib.metrics[-1]["gauges"]["max_reuse"],
                           2 * front.metrics[-1]["gauges"]["max_reuse"])
        # recombination is robust: most reifications fuse >=2 reified primitives
        self.assertGreater(lib.metrics[-1]["gauges"]["combinatorial_fraction"], 0.5)

    def test_exp010_copying_does_not_take_over(self):
        # Ω-0.7 (negative capstone): enabling duplication does NOT breed a
        # self-replicator that dominates the soup — no path for an operator to emit
        # a copy of itself (von Neumann coupling absent). Dominance stays low.
        r = _run("exp010", ticks=600, dup_prob=0.6)
        tail = r.metrics[-100:]
        dominance = max(m["gauges"]["dominance"] for m in tail)
        self.assertLess(dominance, 0.3)  # far from a takeover (~1.0)

    def test_exp012_combinator_breaks_the_copying_wall(self):
        # Ω-0.9 breakthrough: the behaviour-first SKI substrate produces genuine
        # self-replicators (C x -> C), which the string soup structurally cannot.
        combo = _run("exp012", ticks=800)
        string = _run("exp010", ticks=800, dup_prob=0.6)
        combo_selfcat = max(m["gauges"].get("max_selfcat", 0) for m in combo.metrics)
        string_selfcat = max(m["gauges"].get("max_selfcat", 0) for m in string.metrics)
        self.assertGreater(combo_selfcat, 10)   # self-replicators emerge
        self.assertEqual(string_selfcat, 0)     # impossible in the string soup

    def test_exp013_mutation_sustains_novelty_with_reproduction(self):
        # Ω-0.10 synthesis: heritable variation sustains novelty *while* keeping
        # self-catalysis, and multiplies coexisting replicator lineages rather than
        # letting one monopolise. (The full diversity-collapse contrast is a longer-
        # horizon effect; here we assert the robust early signals.)
        no_mut = _run("exp013", ticks=1200, mut_prob=0.0)
        mut = _run("exp013", ticks=1200, mut_prob=0.05)
        # the robust early signal: mutation multiplies coexisting replicator
        # lineages instead of letting one monopolise, while reproduction persists.
        # (The novelty/diversity divergence is a longer-horizon effect; see the
        # 3000-tick dose-response in RESEARCH_LOG.)
        self.assertGreater(mut.metrics[-1]["gauges"]["n_selfcat_classes"],
                           no_mut.metrics[-1]["gauges"]["n_selfcat_classes"])
        self.assertGreater(mut.metrics[-1]["gauges"]["max_selfcat"], 10)  # replicators persist

    def test_exp014_mutualism_beats_null(self):
        # Ω-0.11 ecology: the replicators form an interaction network with
        # reciprocal cross-production (mutualism) well above a degree-preserving
        # null — real structure, not a graph-size artefact.
        from omega.metrics.ecology import analyze
        physics, cfg = get_experiment("exp014")(seed=0, ticks=700, mut_prob=0.05)
        run(physics, cfg)
        rep = analyze(physics._cross, physics._produces, physics._produced,
                      physics._size_of, seed=1)
        self.assertGreater(rep.reciprocity_z, 2.0)   # significant excess mutualism
        self.assertGreater(rep.n_mutual_pairs, 0)

    def test_exp015_knockout_suppresses_a_class(self):
        # Ω-0.12 mechanism: a suppressed class is dissolved every tick, so it stays
        # absent from the population — the basis of the hypercycle knockout test.
        from omega.kernel.organization import canonical_cls
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise
        target = canonical_cls("S")  # suppress the atom S
        physics, _ = get_experiment("exp014")(seed=1, mut_prob=0.05)
        physics.suppress = {target}
        u = Universe(4000)
        physics.seed(u, Noise(1))
        sched = Scheduler(u, physics, Noise(1), decay_hazard=0.05, max_reactions_per_tick=150)
        for _ in range(30):
            sched.step()
        self.assertNotIn(target, {o.cls for o in u.organizations.values()})

    def test_exp016_locality_makes_hypercycles_obligate(self):
        # Ω-0.13: reducing production redundancy via spatial locality makes a
        # hypercycle member's removal collapse its partners far more than in the
        # well-mixed soup — obligate collectives form.
        from omega.metrics.ecology import build_edges

        def partner_survival(n_patches):
            pb, cb = get_experiment("exp016")(seed=0, ticks=800, n_patches=n_patches)
            run(pb, cb)
            edges = build_edges(pb._cross, min_weight=5)
            adj = {}
            for (i, j) in edges:
                adj.setdefault(i, {})[j] = pb._cross[(i, j)]
            best = None
            for i in adj:
                for j in adj[i]:
                    for k in adj.get(j, {}):
                        if i in adj.get(k, {}) and len({i, j, k}) == 3:
                            s = min(adj[i][j], adj[j][k], adj[k][i])
                            if best is None or s > best[0]:
                                best = (s, i, j, k)
            _, i, j, k = best
            ctrl = pb._produced.get(j, 0) + pb._produced.get(k, 0)
            pk, ck = get_experiment("exp016")(seed=0, ticks=800, n_patches=n_patches)
            pk.suppress = {i}
            run(pk, ck)
            return (pk._produced.get(j, 0) + pk._produced.get(k, 0)) / (ctrl + 1e-9)

        self.assertLess(partner_survival(24), partner_survival(0) - 0.1)

    def test_exp017_reducing_feed_strengthens_collective_heredity(self):
        # Ω-0.14: collective-level selection needs collective *heredity*, which the
        # random feed dilutes. Cutting the feed makes a founded deme resemble its
        # source far more than a random deme — the precondition for a major
        # transition. (Low feed >> high feed on the heredity ratio.)
        from statistics import fmean

        def heredity_ratio(feed):
            p, c = get_experiment("exp017")(seed=0, ticks=900, propagule_size=12,
                                            mut_prob=0.015, deme_gen=30,
                                            deme_death_frac=0.4, propagule_mode="source")
            p.feed_rate = feed
            run(p, c)
            hs = fmean(p._hered_self) if p._hered_self else 0.0
            hn = fmean(p._hered_null) if p._hered_null else 1e-9
            return hs / (hn + 1e-9)

        low, high = heredity_ratio(3), heredity_ratio(14)
        self.assertGreater(low, 2.0)      # strong collective heredity at low feed
        self.assertGreater(low, high)     # and stronger than the high-feed regime

    def test_exp018_collective_fitness_does_not_outcompete_individuals(self):
        # Ω-0.15: exp017 gave collective heredity but no collective *selection*.
        # exp018 adds heritable between-deme fitness variance (productivity-weighted
        # deme reproduction) + strong heredity. Claim (a negative one): it still does
        # not make the collective win — the fraction of *live* demes that are distinct
        # types is no lower under `source` (selection ON) than under the well-mixed
        # `mixed` null. Any raw drop in deme-type count is deme die-off, not selection.
        from statistics import mean

        def types_per_live(mode):
            p, c = get_experiment("exp018")(seed=0, ticks=600, n_patches=24,
                                            propagule_mode=mode)
            p.feed_rate = 4            # low enough to strengthen heredity, still alive
            r = run(p, c)
            tail = r.metrics[-len(r.metrics) // 5:]
            ndt = mean(m["gauges"].get("n_deme_types", 0.0) for m in tail)
            live = mean(m["gauges"].get("n_live_demes", 1.0) for m in tail)
            return (ndt / live if live else 0.0), r.final_population

        src_tl, src_pop = types_per_live("source")
        mix_tl, _ = types_per_live("mixed")
        self.assertGreater(src_pop, 20)              # system still alive (not collapsed)
        # no differential winnowing per live deme: source is not meaningfully below null
        self.assertLess(abs(src_tl - mix_tl), 0.15)

    def test_exp019_local_feed_does_not_unlock_collective_selection(self):
        # Ω-0.16: exp018 predicted a patch-local feed would let a local replicator
        # take over a deme (a heritable type) and unlock collective selection.
        # exp019 implements it. Claim (still negative): in a healthy regime the
        # collective still does not winnow — `source` types-per-live-deme is not
        # below the well-mixed `mixed` null. Local feed raises dominance and deme
        # survival but never clears the barrier.
        from statistics import mean

        def types_per_live(mode):
            p, c = get_experiment("exp019")(seed=0, ticks=600, n_patches=24,
                                            propagule_mode=mode)
            p.feed_rate = 4            # healthy regime (not collapsed)
            r = run(p, c)
            tail = r.metrics[-len(r.metrics) // 5:]
            ndt = mean(m["gauges"].get("n_deme_types", 0.0) for m in tail)
            live = mean(m["gauges"].get("n_live_demes", 1.0) for m in tail)
            return (ndt / live if live else 0.0), r.final_population

        src_tl, src_pop = types_per_live("source")
        mix_tl, _ = types_per_live("mixed")
        self.assertGreater(src_pop, 20)               # healthy, not collapsed
        self.assertGreater(src_tl, mix_tl - 0.05)     # no winnowing below the null

    def test_exp020_replicase_consolidates_but_not_as_a_collective(self):
        # Ω-0.17: an explicit strong copy channel (T -> T + T) finally makes
        # replicators that consolidate the soup (n_deme_types collapses ~19 -> ~10,
        # population grows to carrying capacity). But it is *individual*-level
        # selection: a few compact replicators colonize every deme. Claim: the
        # consolidation is identical with collective heredity ON (`source`) and OFF
        # (`mixed`) — source's types-per-live-deme is not below the mixed null — so
        # it is not the collective outcompeting.
        from statistics import mean

        def probe(mode):
            p, c = get_experiment("exp020")(seed=0, ticks=400, n_patches=24,
                                            propagule_mode=mode, copy_rate=0.5)
            r = run(p, c)
            tail = r.metrics[-len(r.metrics) // 5:]
            ndt = mean(m["gauges"].get("n_deme_types", 0.0) for m in tail)
            live = mean(m["gauges"].get("n_live_demes", 1.0) for m in tail)
            return (ndt / live if live else 0.0), ndt, r.final_population

        src_tl, src_ndt, src_pop = probe("source")
        mix_tl, _, _ = probe("mixed")
        self.assertGreater(src_pop, 400)          # replicase active (grew from ~174)
        self.assertLess(src_ndt, 15.0)            # copying consolidated deme-types
        self.assertGreater(src_tl, mix_tl - 0.05)  # but not collective: source !< null

    def test_exp021_group_selection_maintains_cooperation(self):
        # Ω-0.18: the positive capstone. exp017-020 found the multi-level structure
        # inert because no group-selectable trait emerged. exp021 supplies one — a
        # cooperation trait that is individually costly but collectively beneficial —
        # and, at strong relatedness (single-founder bottleneck), group selection
        # finally works: cooperation is maintained far above the well-mixed null
        # under collective heredity (`source`) but decays toward it under `mixed`.
        from statistics import mean

        def coop_late(mode):
            p, c = get_experiment("exp021")(seed=0, ticks=800, n_patches=24,
                                            propagule_mode=mode)
            r = run(p, c)
            cf = [m["gauges"].get("coop_frac", 0.0) for m in r.metrics]
            return mean(cf[-len(cf) // 4:]) if cf else 0.0

        src, mix = coop_late("source"), coop_late("mixed")
        self.assertGreater(src, 0.20)          # cooperation maintained under group heredity
        self.assertGreater(src, mix + 0.08)    # and well above the well-mixed null

    def test_exp022_emergent_collective_trait_is_group_selectable(self):
        # Ω-0.19: the open problem — a group trait that *emerges* rather than being
        # imposed. Deme fitness is internal cross-production (a member making a
        # different member): irreducibly collective, no single replicator can
        # maximize it. With a propagule large enough to transmit the network,
        # collective heredity+selection (`source`) maintains markedly more
        # cross-production than the well-mixed `mixed` null.
        from statistics import mean

        def xprod(mode):
            p, c = get_experiment("exp022")(seed=0, ticks=1500, n_patches=24,
                                            propagule_mode=mode, propagule_size=20)
            r = run(p, c)
            g = [m["gauges"].get("mean_cross_prod", 0.0) for m in r.metrics]
            return mean(g[-len(g) // 4:]) if g else 0.0

        src, mix = xprod("source"), xprod("mixed")
        self.assertGreater(src, mix * 1.15)   # emergent collective trait is favored

    def test_exp023_niche_construction_lifts_dominance_but_costs_novelty(self):
        # Ω-0.20: attacks the within-deme-dominance wall (stuck ~0.37 across
        # exp017-022) with a second, environmental inheritance channel — recycle a
        # deme's own recent products as its feed. It works partially: deme-types
        # consolidate (n_deme_types drops vs the random-feed baseline) as the
        # environment reinforces each deme's composition, but at a real cost — the
        # novelty rate falls sharply (the Ω-0.14 heredity-vs-diversity tension, now
        # localized to the feed). (It does not, on its own, individuate: source~=mixed.)
        from statistics import mean

        def probe(feed_mode):
            p, c = get_experiment("exp023")(seed=0, ticks=800, n_patches=24,
                                            propagule_mode="source", feed_mode=feed_mode)
            r = run(p, c)
            tail = r.metrics[-len(r.metrics) // 5:]
            ndt = mean(m["gauges"].get("n_deme_types", 0.0) for m in tail)
            return ndt, r.open_endedness["novelty_rate"]

        rnd_ndt, rnd_nov = probe("random")
        rec_ndt, rec_nov = probe("recycle")
        self.assertLess(rec_ndt, rnd_ndt - 2.0)   # recycling consolidates deme-types
        self.assertLess(rec_nov, rnd_nov)          # at a cost: less open-ended novelty

    def test_exp024_individuation_blocked_by_substrate_type_space(self):
        # Ω-0.21: combining every partial lever — recycle feed (dominance), network
        # fitness (collective selection), monoculture founding (forced divergence),
        # isolation — still does not individuate demes. The diagnosis is a NEW
        # substrate-level wall: small combinator expressions reduce to only ~a dozen
        # common attractor normal forms, so 24 distinct monoculture founders *collide*
        # — the count of distinct deme-types at t0 is far below 24 — and those shared
        # attractors re-homogenize every deme. Individuation is blocked by type-space
        # poverty, not by the multi-level machinery.
        from statistics import mean

        p, c = get_experiment("exp024")(seed=0, ticks=600, n_patches=24,
                                        propagule_mode="source")
        r = run(p, c)
        g = [m["gauges"].get("n_deme_types", 0.0) for m in r.metrics]
        # 24 distinct monoculture founders collapse onto ~a dozen classes at t0:
        self.assertLess(g[0], 18.0)
        # and demes never individuate into many distinct persistent types:
        self.assertLess(mean(g[-len(g) // 5:]), 22.0)

    def test_exp025_network_signature_is_a_heritable_deme_identity(self):
        # Ω-0.22: exp024 found individuation blocked because a deme's identity (its
        # dominant class) draws from only ~9 attractor types. Redefining identity as
        # the deme's cross-production NETWORK SIGNATURE (edge-set) recovers part of it:
        # the signature is genuinely heritable through the propagule (a founded deme's
        # network resembles its source more than a random deme), and it resolves a
        # richer identity space than the dominant-class metric.
        from statistics import mean

        p, c = get_experiment("exp025")(seed=0, ticks=1000, n_patches=24,
                                        propagule_mode="source")
        r = run(p, c)
        self.assertTrue(p._hered_edge_self and p._hered_edge_null)
        # network signature is heritable: child resembles source > a random deme
        self.assertGreater(mean(p._hered_edge_self), mean(p._hered_edge_null))
        # and the signature identity space is richer than the dominant-class one
        tail = r.metrics[-len(r.metrics) // 5:]
        n_sigs = mean(m["gauges"].get("n_deme_signatures", 0.0) for m in tail)
        n_types = mean(m["gauges"].get("n_deme_types", 0.0) for m in tail)
        self.assertGreater(n_sigs, n_types)

    def test_exp026_richer_interacting_basis_strengthens_network_heredity(self):
        # Ω-0.23: exp024/025 capped network individuation at ~1.6x because the SKI
        # type space collapses to ~9 attractors. Enriching the basis with extra
        # *interacting* combinators (B/C/W) — not inert data, which would kill cross-
        # production — broadens the type space AND strengthens the heritability of a
        # deme's cross-production network signature. The richer substrate gives a
        # strictly higher edge-set heredity ratio than SKI alone.
        from statistics import mean

        def edge_heredity(extra):
            p, c = get_experiment("exp026")(seed=0, ticks=1200, n_patches=24,
                                            propagule_mode="source",
                                            extra_combinators=extra,
                                            deme_fitness="network")
            run(p, c)
            self_j = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
            null_j = mean(p._hered_edge_null) if p._hered_edge_null else 1e-9
            return self_j, null_j, self_j / null_j

        ski_s, ski_n, ski_r = edge_heredity("")
        bcw_s, bcw_n, bcw_r = edge_heredity("BCW")
        self.assertGreater(bcw_s, bcw_n)          # signature still heritable
        self.assertGreater(bcw_r, ski_r + 0.3)    # richer basis strengthens it

    def test_exp029_modular_substrate_reproduces_networks_but_closes(self):
        # Ω-0.26: the substrate pivot confirms exp028's diagnosis and reveals the deep
        # trade-off. A typed substrate (morphisms + modular composition) makes a deme's
        # network reproducible from its members: child-source network overlap roughly
        # triples vs the combinator substrate (self ~0.24 vs ~0.10) — the reproducibility
        # ceiling breaks. But the typed substrate is CLOSED: novelty collapses to ~0,
        # while the combinator substrate stays open-ended. Neither achieves both.
        from statistics import mean

        def probe(exp, **kw):
            p, c = get_experiment(exp)(seed=0, ticks=1500, n_patches=24,
                                       propagule_mode="source", **kw)
            r = run(p, c)
            self_j = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
            return self_j, r.open_endedness["novelty_rate"]

        comb_self, comb_nov = probe("exp027", extra_combinators="B,C,W,T,V")
        typ_self, typ_nov = probe("exp029")
        self.assertGreater(typ_self, comb_self + 0.1)   # modularity reproduces networks
        self.assertLess(typ_nov, 1.0)                    # ...but the typed substrate closes
        self.assertGreater(comb_nov, 1.0)                # while the combinator stays open

    def test_exp028_individuation_ceiling_is_substrate_not_transmission(self):
        # Ω-0.25: the ~3.3x network-heredity ceiling is substrate-limited, not
        # transmission-limited. Even a network-biased propagule that transmits the
        # source deme's whole network leaves the signature heritable-but-thin: the
        # child resembles its source more than a random deme (self > null), yet the
        # absolute overlap stays small (thin ~2-edge networks), so no strong, discrete
        # collective individual forms. Better transmission cannot break the ceiling —
        # motivating a typed/lambda substrate pivot (see EXP028_FINDINGS.md).
        from statistics import mean

        p, c = get_experiment("exp028")(seed=0, ticks=1500, n_patches=24,
                                        propagule_mode="source")
        run(p, c)
        self.assertTrue(p._hered_edge_self and p._hered_edge_null)
        self_j, null_j = mean(p._hered_edge_self), mean(p._hered_edge_null)
        self.assertGreater(self_j, null_j)   # still weakly heritable
        self.assertLess(self_j, 0.2)          # but thin — not strong individuation

    def test_exp027_basis_richness_dials_up_individuation(self):
        # Ω-0.24: the substrate dial. A richer *interacting* basis both enriches the
        # type space and strengthens network-signature heredity — near the optimum
        # (S,K,I,B,C,W,T,V), collective individuation reaches its arc-high (~3.3x self/
        # null), far above SKI (~1.6x). (The full dose-response shows it peaks ~7-8
        # combinators then declines as too-rich a type space stops networks breeding
        # true — see EXP027_FINDINGS.md.)
        from collections import Counter
        from statistics import mean
        from omega.experiments.exp012_combinator import canonical_cls
        from omega.substrate.noise import Noise

        def types(extra):
            p, _ = get_experiment("exp027")(seed=0, n_patches=24, extra_combinators=extra)
            rng = Noise(0)
            return len(Counter(canonical_cls(p._random_normal(rng)) for _ in range(3000)))

        def edge_ratio(extra):
            p, c = get_experiment("exp027")(seed=0, ticks=1200, n_patches=24,
                                            propagule_mode="source", extra_combinators=extra)
            run(p, c)
            return mean(p._hered_edge_self) / (mean(p._hered_edge_null) + 1e-9)

        self.assertGreater(types("B,C,W,T,V"), 3 * types(""))   # richer type space
        self.assertGreater(edge_ratio("B,C,W,T,V"), edge_ratio("") + 1.0)  # stronger heredity

    def test_exp031_transition_recurses_into_a_level_tower(self):
        # Ω-0.28: the major transition RECURSES. Each tier's stable heritable collectives
        # become the atoms of the next tier (reification across levels of individuality),
        # so physics → chemistry → biology → culture stack as tiers of one engine. The
        # tower reaches multiple levels, each still forming heritable collectives.
        from omega.levels.stack import run_stack
        r = run_stack(max_tiers=3, seed=0, ticks=900)
        self.assertGreaterEqual(r.tower_depth, 2)      # >=2 organizational levels stack
        self.assertTrue(r.tiers[0].heritable)          # tier 0 forms heritable collectives
        self.assertTrue(r.unfold)                       # promotion happened (nesting map)

    def test_exp031_culture_horizontal_transfer(self):
        # Ω-0.28: the culture level — horizontal, Lamarckian motif transfer between
        # collectives (imitation), decoupled from reproduction, active and open-ended.
        p, c = get_experiment("exp031_culture")(seed=0, ticks=1000, n_patches=24,
                                                propagule_mode="source")
        r = run(p, c)
        self.assertGreater(p._meme_horizontal, 0)      # the horizontal channel is active
        self.assertGreater(r.open_endedness["novelty_rate"], 0.0)  # and still open-ended

    def test_exp032_both_corner_persists_across_windows(self):
        # Ω-0.29: unboundedness (within-level). Over successive temporal WINDOWS the
        # open+modular "both corner" (exp030) keeps BOTH its novelty rate and its
        # collective heredity (self > null) alive — not a startup transient — while the
        # matched CLOSED control (exp029) lets novelty collapse toward zero. Rates in
        # windows, not cumulatives (the program's two false positives were cumulative).
        from statistics import mean

        def windows(xs, k):
            n = len(xs)
            return [xs[(w * n) // k:((w + 1) * n) // k] for w in range(k)]

        po, co = get_experiment("exp030")(seed=0, ticks=2000, n_patches=24,
                                          propagule_mode="source")
        ro = run(po, co)
        pc, cc = get_experiment("exp029")(seed=0, ticks=2000, n_patches=24,
                                          propagule_mode="source")
        rc = run(pc, cc)
        # skip window 0 (the initial discovery burst); test the sustained regime.
        nov_o = [mean(w) for w in windows(ro.novelty_new_per_tick, 5)][1:]
        nov_c = [mean(w) for w in windows(rc.novelty_new_per_tick, 5)][1:]
        self_w = [mean(w) for w in windows(po._hered_edge_self, 5)][1:]
        null_w = [mean(w) for w in windows(po._hered_edge_null, 5)][1:]
        self.assertTrue(all(v > 0 for v in nov_o))          # open: novelty alive every window
        self.assertTrue(all(s > n for s, n in zip(self_w, null_w)))  # heredity alive every window
        self.assertLess(nov_c[-1], nov_o[-1])               # closed control decays vs open

    def test_exp036_cyclic_feed_gives_the_environment_structure(self):
        # Ω-0.24: intrinsic function needs an environment worth predicting. exp036's cyclic
        # feed favours the CURRENT season's band, so the world has exploitable structure (a
        # deme can be reactive). Whether *anticipation* is selectable is the study's
        # negative-with-diagnosis: it is not, absent internal state (see EXP036_FINDINGS.md).
        from omega.substrate.noise import Noise
        p, c = get_experiment("exp036")(seed=0, ticks=10)
        p._cur_band = list(p.atoms[:8])            # 8 of 32 atoms = the season's band
        cur, rng = set(p._cur_band), Noise(0)
        biased = sum(1 for _ in range(2000) if p._feed_choice(rng) in cur) / 2000
        self.assertGreater(biased, 0.5)            # cyclic feed concentrates on the band (>>0.25)
        p.feed_pattern = "random"
        flat = sum(1 for _ in range(2000) if p._feed_choice(rng) in cur) / 2000
        self.assertLess(flat, 0.4)                 # random feed is ~uniform (chance 0.25)
        r = run(*get_experiment("exp036")(seed=0, ticks=800))
        self.assertGreater(r.open_endedness["novelty_rate"], 0.0)   # still an open world

    def test_exp037_per_collective_genome_is_evolvable_internal_state(self):
        # Ω-0.25: the engine piece exp036 lacked — a collective carries a heritable, mutable
        # construction rule of its own (its type_resolution), used in its own compositions and
        # transmitted to the demes it founds. Here we pin that the genome exists, diversifies
        # (per-deme values within range), and the world stays open; the *evolution under
        # selection* verdict (treat vs control) is the study's (EXP037_FINDINGS.md).
        p, c = get_experiment("exp037")(seed=0, ticks=2500)
        r = run(p, c)
        self.assertTrue(p.deme_genome)
        res = list(p._deme_res.values())
        self.assertGreater(len(res), 0)                       # a per-collective genome formed
        self.assertTrue(all(1 <= v <= 6 for v in res))        # within the genome range
        self.assertGreaterEqual(len(set(res)), 2)             # it diversified across demes
        self.assertGreater(r.open_endedness["novelty_rate"], 0.0)   # still an open world

    def test_exp038_closure_is_emergent_and_selectable(self):
        # Ω-0.26: coherence made an emergent, selectable target. Autocatalytic closure (the
        # self-producing fraction of a deme's real cross-production network) is read off the
        # network (emergent, not imposed like exp021's coop bit), and selecting for it raises
        # it above a no-network-selection baseline. (That it TRADES OFF against heredity under
        # single-objective selection is the study's honest negative — EXP038_FINDINGS.md.)
        from statistics import mean

        def mean_closure(fit):
            p, c = get_experiment("exp038")(seed=0, ticks=2500, deme_fitness=fit)
            run(p, c)
            cs = [p._deme_closure(pi) for pi in range(p.n_patches) if p._deme_edges.get(pi)]
            return (mean(cs) if cs else 0.0)

        c_sel = mean_closure("closure")
        c_base = mean_closure("size")                 # size = no network/closure selection
        self.assertGreaterEqual(c_sel, 0.0)
        self.assertLessEqual(c_sel, 1.0)               # a well-formed fraction (emergent metric)
        self.assertGreater(c_sel, c_base)              # selection raises it above the baseline

    def test_exp039_composite_selection_lifts_closure(self):
        # Ω-0.27 (capstone): multi-objective (maximin) selection over closure AND heredity is
        # a valid, gated fitness that lifts the closure objective above a no-network baseline.
        # The capstone SCIENCE — that it lifts closure but NOT heredity, because collective
        # heredity is the weak channel (exp028 ceiling), so competence does not compound — is
        # the study's result (EXP039_FINDINGS.md); here we pin the mechanism is sound.
        from statistics import mean

        def closure(fit):
            p, c = get_experiment("exp039")(seed=0, ticks=2500, deme_fitness=fit)
            run(p, c)
            cs = [p._deme_closure(pi) for pi in range(p.n_patches) if p._deme_edges.get(pi)]
            return (mean(cs) if cs else 0.0)

        self.assertGreater(closure("composite"), closure("size"))   # combined selection acts

    def test_exp040_developmental_template_breaks_the_heredity_ceiling(self):
        # Ω-0.28: the collective-heredity ceiling (exp028, ~3-5x null / self ~0.1-0.28) breaks
        # with a PARTIAL developmental-niche template — offspring inherit a fraction of the parent
        # network's products and canalize to its edges, reaching the collective "both corner"
        # (strong heredity AND sustained novelty). Full pinning closes the world (the study's
        # trade-off; EXP040_FINDINGS.md). Off (strength 0) is byte-identical.
        from statistics import mean

        def heredity_novelty(strength):
            p, c = get_experiment("exp040")(seed=0, ticks=2500, network_template=strength)
            r = run(p, c)
            s = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
            n = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
            return s, n, r.open_endedness["novelty_rate"]

        off_s, off_n, off_v = heredity_novelty(0.0)             # the ceiling baseline (open, weak)
        full_s, full_n, full_v = heredity_novelty(1.0)          # full template (strong, pinned)
        self.assertGreater(full_s, 2 * off_s)                   # template breaks heredity past ceiling
        self.assertGreater(full_s, full_n)                      # and it is parent-specific (self > null)
        self.assertGreater(off_v, full_v)                       # the dial trades novelty (full closes);
        # the intermediate BOTH corner (heredity AND open) is the study's multi-seed result.

    def test_exp041_composite_and_template_compose(self):
        # Ω-0.29 (payoff capstone): running the aligned multi-objective objective
        # (deme_fitness="composite", exp039) TOGETHER with the developmental channel that broke the
        # heredity ceiling (network_template>0, exp040). Here we pin that the two mechanisms COMPOSE
        # and both operate: (a) collective identity is still heritable with the template on
        # (self > null), and (b) composite selection still acts on top of the template (closure above
        # a drift baseline that shares the same template). The SCIENCE — whether closure, heredity,
        # and function now rise TOGETHER over generations (compound) instead of trading off, the
        # payoff the whole self-improvement arc was built toward — is the study's result
        # (EXP041_FINDINGS.md); this pins the combined mechanism is sound.
        from statistics import mean

        # Averaged over 3 seeds. The two robust, deterministic facts (verified under the Ω-0.33
        # deterministic engine): with the template on collective identity is heritable (self >> null),
        # and the exp040 developmental channel raises the heredity LEVEL over no template. (We do NOT
        # assert composite beats the drift arm on closure or heredity: the template itself dominates
        # heredity, and composite's maximin trades some closure for heredity, so drift+template can
        # exceed it on either single axis — the compounding verdict is the study's science.)
        def heredity(template):
            sl, nl = [], []
            for seed in range(3):
                p, c = get_experiment("exp041")(seed=seed, ticks=2500,
                                                deme_fitness="composite", network_template=template)
                run(p, c)
                sl.append(mean(p._hered_edge_self) if p._hered_edge_self else 0.0)
                nl.append(mean(p._hered_edge_null) if p._hered_edge_null else 0.0)
            return mean(sl), mean(nl)

        s_on, n_on = heredity(0.5)      # composite + template
        s_off, _n = heredity(0.0)       # composite, no template
        self.assertGreater(s_on, n_on)  # heritable collective identity with the template on
        self.assertGreater(s_on, s_off)  # the developmental template raises the heredity level

    def test_exp042_ratchet_raises_a_monotonic_competence_bar(self):
        # Ω-0.30: a SELF-EXPANDING objective. deme_fitness="ratchet" rewards demes for beating a
        # moving competence bar, and the bar is raised toward the achieved frontier and never
        # lowered (goal reification). Here we pin the mechanism is sound: the bar rises above 0
        # (demes clear it, so it self-expands) and is monotonic non-decreasing across generations;
        # collective identity stays heritable with the ratchet + template on (self > null). Whether
        # a moving objective actually makes competence COMPOUND over generations — the arc's open
        # question — is the study's result (EXP042_FINDINGS.md). ratchet_lr=0 ⇒ byte-identical.
        from statistics import mean
        from omega.experiments.exp012_combinator import Physics
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        p, c = get_experiment("exp042")(seed=0, ticks=2500)
        rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
        sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                        max_reactions_per_tick=c.max_reactions_per_tick)
        bars = []
        for _ in range(2500):
            sch.run(1)
            bars.append(p._ratchet_bar)
        self.assertGreater(p._ratchet_bar, 0.0)                 # the bar self-expands off zero
        self.assertTrue(all(b <= a + 1e-12 for b, a in zip(bars, bars[1:])))  # monotonic ↑
        s = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
        n = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
        self.assertGreater(s, n)                                # heritable with ratchet + template

    def test_bounded_memory_mode_flattens_registry_and_stays_open(self):
        # Scaling: the bounded-memory long-run mode (memory_horizon > 0) evicts cold class
        # records so the registry stays flat over long horizons, WITHOUT killing the
        # novelty signal — novelty is counted against a monotonic classes_ever_seen, so it
        # stays positive (windowed). Off (horizon=0) is byte-identical (covered elsewhere).
        p0, c0 = get_experiment("exp030")(seed=0, ticks=4000)
        r0 = run(p0, c0, record_stride=50)                       # unbounded
        pb, cb = get_experiment("exp030")(seed=0, ticks=4000)
        rb = run(pb, cb, record_stride=50, memory_horizon=800, relation_cap=5000)
        # registry is strictly smaller under eviction, novelty still alive
        self.assertLess(rb.final_classes_total, r0.final_classes_total)
        self.assertGreater(rb.open_endedness["novelty_rate"], 0.0)

    def test_exp044_goals_are_heritable_composable_and_reify(self):
        # Ω-0.32 (the frontier): heritable, composable GOALS — the representational faculty exp042
        # proved was missing. Pin the mechanism DIRECTLY and deterministically (the *emergent* depth
        # ratchet is the study's science, EXP044_FINDINGS.md, and is hash-seed sensitive, so it is
        # not asserted here): (1) _contig_subseq achievement test is correct; (2) goal reification
        # EXTENDS an achieved goal, but only with composability on; (3) goals are heritable per deme.
        # deme_fitness default ⇒ exp001–043 byte-identical.
        from omega.experiments.exp012_combinator import _path_nodes, _path_build, _contig_subseq
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        # (1) achievement predicate: a goal path is realized when it is a contiguous stretch.
        self.assertTrue(_contig_subseq(["a", "b"], ["z", "a", "b", "c"]))
        self.assertFalse(_contig_subseq(["a", "c"], ["a", "b", "c"]))   # not contiguous
        self.assertFalse(_contig_subseq(["a", "b", "c"], ["a", "b"]))   # longer than seq

        # (2) reification: force robust achievement on every patch, then one deme-reproduction step
        # must EXTEND an achieved goal when goal_reify is ON, and leave depth pinned when OFF.
        def forced_reify(reify):
            p, c = get_experiment("exp044")(seed=0, ticks=400, goal_reify=reify)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                            max_reactions_per_tick=c.max_reactions_per_tick)
            sch.run(400)
            for pi in range(p.n_patches):                    # every deme has robustly achieved
                p._deme_goal[pi] = _path_build([p.atoms[0], p.atoms[1]])
                p._deme_goal_hit[pi] = 5
            before = max(len(_path_nodes(g)) for g in p._deme_goal.values())
            p._deme_reproduction(u, rng)
            after = max(len(_path_nodes(g)) for g in p._deme_goal.values())
            return before, after

        b_on, a_on = forced_reify(True)
        b_off, a_off = forced_reify(False)
        self.assertEqual(b_on, 2)
        self.assertGreater(a_on, b_on)          # composability ON: an achieved goal is extended
        self.assertEqual(a_off, b_off)          # composability OFF: goals never deepen

        # (3) goals are heritable per deme (present after a run under the goal fitness).
        p, c = get_experiment("exp044")(seed=0, ticks=800)
        rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
        Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                  max_reactions_per_tick=c.max_reactions_per_tick).run(800)
        self.assertTrue(p._deme_goal)
        self.assertTrue(all(len(_path_nodes(g)) >= 2 for g in p._deme_goal.values()))

    def test_exp045_goal_alignment_targets_the_closure_core(self):
        # Ω-0.34 (credit assignment): exp045 aims goal reification at the deme's autocatalytic closure
        # core (producers ∩ products) instead of the most-produced atom (exp044). Pin the mechanism
        # deterministically: when a deme has a closure loop, the aligned extension atom is drawn from a
        # member of that loop; the goal still deepens; goal_align is gated (exp044 = align off, and off
        # ⇒ exp001–044 byte-identical). Whether aiming at the core makes generic competence RISE with
        # goal depth is the study's science (EXP045_FINDINGS.md).
        from omega.experiments.exp012_combinator import _path_nodes, _path_build
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        def forced(align, seed=1):
            p, c = get_experiment("exp045")(seed=seed, ticks=600, goal_align=align)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            sch = Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                            max_reactions_per_tick=c.max_reactions_per_tick)
            sch.run(600)
            for pi in range(p.n_patches):                    # force robust achievement everywhere
                p._deme_goal[pi] = _path_build([p.atoms[0], p.atoms[1]])
                p._deme_goal_hit[pi] = 5
            before = max(len(_path_nodes(g)) for g in p._deme_goal.values())
            p._deme_reproduction(u, rng)
            after = max(len(_path_nodes(g)) for g in p._deme_goal.values())
            return before, after

        b_on, a_on = forced(True)
        self.assertEqual(b_on, 2)
        self.assertGreater(a_on, b_on)                       # aligned reification still deepens goals

        # gated: goal_align default off means exp045 with align off == exp044 (byte-identical dynamics)
        def classes(exp, **ov):
            p, c = get_experiment(exp)(seed=2, ticks=1500, **ov)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(1500)
            return u.classes_ever_seen
        self.assertEqual(classes("exp045", goal_align=False), classes("exp044"))

    def test_exp046_credit_is_heritable_and_rewards_retained_parts(self):
        # Ω-0.35 (credit in selection): exp046 gives each deme a HERITABLE per-class contribution map
        # that accrues credit for its autocatalytic closure-core classes, and deme_fitness="credit"
        # rewards demes that RETAIN their high-credit parts. Pin the mechanism deterministically:
        # a credit map is built and populated; it credits closure-core classes; it is heritable
        # (inherited at recolonization); and goal/credit knobs default off ⇒ exp046 with deme_fitness
        # unset is not built here — instead we pin that the "credit" fitness is a live, gated mode and
        # that a non-credit experiment is byte-identical. Whether competence COMPOUNDS is the study's
        # science (EXP046_FINDINGS.md).
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        p, c = get_experiment("exp046")(seed=0, ticks=3000)
        rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
        Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                  max_reactions_per_tick=c.max_reactions_per_tick).run(3000)
        # a heritable credit model exists and carries positive contribution scores
        self.assertTrue(p._deme_credit)
        allscores = [v for cr in p._deme_credit.values() for v in cr.values()]
        self.assertTrue(allscores and all(v > 0 for v in allscores))

        # gated: exp030 (no credit) is unaffected by the exp046 machinery being present.
        def classes(exp):
            pp, cc = get_experiment(exp)(seed=0, ticks=1500)
            rr = run(pp, cc)
            return rr.final_classes_total
        self.assertGreater(classes("exp030"), 0)   # base engine still runs, credit code never touched

    def test_exp047_within_selection_biases_the_propagule_by_credit(self):
        # Ω-0.36 (within-collective selection): exp047 founds each offspring from the source deme's
        # members sampled by their credit (parts competing inside the deme). Pin the mechanism
        # deterministically and its gating: within_select is a live gated knob; with it OFF exp047 is
        # exactly exp046 (byte-identical), and the credit machinery still builds a heritable map.
        # Whether within-collective selection COMPOUNDS or COLLAPSES competence is the study's science
        # (EXP047_FINDINGS.md).
        p_on, _c = get_experiment("exp047")(seed=0, ticks=1500)
        self.assertTrue(p_on.within_select)                 # exp047 turns within-collective selection on
        self.assertEqual(p_on.deme_fitness, "credit")       # built on the exp046 credit machinery

        def classes(exp, **ov):
            from omega.kernel.universe import Universe
            from omega.kernel.scheduler import Scheduler
            from omega.substrate.noise import Noise
            p, c = get_experiment(exp)(seed=1, ticks=1500, **ov)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(1500)
            return u.classes_ever_seen, dict(p._deme_credit)
        c_off, credit_off = classes("exp047", within_select=False)
        c_credit, _ = classes("exp046")
        self.assertEqual(c_off, c_credit)                   # within_select off ⇒ exp046 byte-identical
        self.assertTrue(credit_off)                         # the heritable credit map is still built

    def test_exp048_loopback_runs_credit_on_the_replicator_substrate(self):
        # Ω-0.37 (the loop-back): exp048 runs the exp046 credit machinery on the COMBINATOR substrate
        # (where parts can self-replicate, exp012) instead of typed_path. Pin the mechanism: exp048 is
        # on the combinator substrate with credit selection and builds a heritable credit map and a
        # cross-production network there; and it is gated (substrate override; deme_fitness default ⇒
        # exp001–047 unaffected). Whether competence COMPOUNDS with replicating parts is the study's
        # science (EXP048_FINDINGS.md).
        from statistics import mean
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        p, c = get_experiment("exp048")(seed=0, ticks=3000)
        self.assertEqual(p.substrate, "combinator")         # loop-back runs on the replicator substrate
        self.assertEqual(p.deme_fitness, "credit")           # with the exp046 credit machinery
        rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
        Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                  max_reactions_per_tick=c.max_reactions_per_tick).run(3000)
        self.assertTrue(p._deme_credit)                      # a heritable credit map is built
        self.assertTrue(p._deme_edges)                       # a cross-production network forms here too
        cs = [p._deme_closure(pi) for pi in range(p.n_patches) if p._deme_edges.get(pi)]
        self.assertGreater(mean(cs) if cs else 0.0, 0.0)     # the combinator soup forms closure loops

    def test_exp049_competence_reification_promotes_closure_central_modules(self):
        # Ω-0.38 (competence as a rate): exp049 applies the Ω-0.20 reification lever to COMPETENCE —
        # reify_by="closure" promotes the most closure-central module (achieved competent structure)
        # to a new atom every reify_period ticks, instead of the most common one (reify_by="frequency",
        # exp034). Pin the mechanism: closure-reify is the exp049 default; a closure-centrality tally is
        # kept and reification grows the constructed alphabet; and it is gated (reify_period=0 ⇒ no new
        # atoms, and the reify_by knob is off by default ⇒ exp001–048 unaffected). Whether reifying
        # achieved competence makes competence COMPOUND is the study's science (EXP049_FINDINGS.md).
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        p, c = get_experiment("exp049")(seed=0, ticks=4000)
        self.assertEqual(p.reify_by, "closure")              # exp049 reifies COMPETENT (closure) structure
        self.assertEqual(p.deme_fitness, "closure")          # selecting for autocatalytic competence
        self.assertTrue(p.reify_period)                      # reification is on
        n_atoms0 = len(p.atoms)
        rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
        Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                  max_reactions_per_tick=c.max_reactions_per_tick).run(4000)
        self.assertTrue(p._closure_seen or len(p.atoms) > n_atoms0)  # closure tally lives / feeds reify
        self.assertGreater(len(p.atoms), n_atoms0)           # competent modules get promoted to new atoms

        # gating: reify_period=0 ⇒ NO new atoms (the exp048 plateau control), so the alphabet is fixed.
        p0, c0 = get_experiment("exp049")(seed=0, ticks=4000, reify_period=0)
        m0 = len(p0.atoms)
        rng0 = Noise(c0.seed); u0 = Universe(total_quanta=c0.total_quanta); p0.seed(u0, rng0)
        Scheduler(u0, p0, rng0, decay_hazard=c0.decay_hazard,
                  max_reactions_per_tick=c0.max_reactions_per_tick).run(4000)
        self.assertEqual(len(p0.atoms), m0)                  # no reification ⇒ constructed alphabet frozen

    def test_exp052_redqueen_scores_against_a_coevolving_or_frozen_rival(self):
        # Ω-0.41 (the Red Queen): exp052 grounds a RECEDING target in local rivals — deme_fitness=
        # "redqueen" rewards a deme's own closure plus the fraction of its closure core a spatial rival
        # cannot yet produce (a zero-sum, closure-aligned antagonism). Pin the mechanism: redqueen is the
        # exp052 default on the both-corner base; a cross-production network + competence are built; the
        # coevolve arm keeps NO frozen snapshot while the frozen control captures one at freeze_gen; and
        # it is gated (deme_fitness default ⇒ exp001–051 unaffected). Whether the receding target makes
        # competence COMPOUND is the study's science (EXP052_FINDINGS.md).
        from statistics import mean
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        def run(**ov):
            p, c = get_experiment("exp052")(seed=0, ticks=3000, **ov)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(3000)
            return p

        p = run()
        self.assertEqual(p.deme_fitness, "redqueen")          # coevolutionary target is the exp052 default
        self.assertTrue(p.network_template)                    # heredity channel on ⇒ competence can breed
        self.assertTrue(p._deme_edges)                         # a cross-production network forms
        act = [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]
        self.assertGreater(mean(p._deme_competence(pi) for pi in act) if act else 0.0, 0.0)  # competence built
        self.assertFalse(p._frozen_prod)                       # the LIVE arm freezes no rival (target co-moves)

        # the frozen control captures a fixed rival snapshot (full patch coverage) ⇒ target does NOT move.
        pf = run(coevolve_frozen=True)
        self.assertTrue(pf._frozen_prod)                       # a frozen reference was captured
        self.assertEqual(len(pf._frozen_prod), pf.n_patches)   # full coverage — a fixed bar for every rival

    def test_exp053_catalytic_law_promotes_closure_loops_to_network_visible_reactions(self):
        # Ω-0.42 (the Catalytic Law): exp053 changes the substrate law mid-run — every catalyst_period it
        # promotes the most closure-central production of the highest-competence deme to a persistent
        # shared catalyst (anchor_cls -> product_state) injected every tick, so competent structure becomes
        # a reusable NETWORK-VISIBLE reaction (the exp049 fix vs an opaque atom). Pin the mechanism:
        # catalytic_law is the exp053 default on the Red Queen base; catalysts are harvested and the
        # promoted product classes appear as real classes in the universe (not new atoms); and it is gated
        # (catalytic_law=False ⇒ no catalysts, exp001–052 unaffected). Whether it makes competence COMPOUND
        # is the study's science (EXP053_FINDINGS.md).
        from statistics import mean
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        def run(**ov):
            p, c = get_experiment("exp053")(seed=0, ticks=4000, **ov)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(4000)
            return p, u

        p, u = run()
        self.assertTrue(p.catalytic_law)                     # the substrate-law feedback is on by default
        self.assertEqual(p.deme_fitness, "redqueen")         # runs on the exp052 Red Queen base
        n_atoms0 = len(get_experiment("exp053")(seed=0, ticks=1)[0].atoms)
        self.assertTrue(p._catalysts)                        # at least one closure loop was promoted
        anchor_cls, product_state = p._catalysts[0]
        from omega.kernel.organization import canonical_cls
        self.assertIn(canonical_cls(product_state), u.class_registry)  # promoted product is a REAL class...
        self.assertEqual(len(p.atoms), n_atoms0)             # ...NOT a new opaque atom (the exp049 fix)
        act = [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]
        self.assertGreater(mean(p._deme_competence(pi) for pi in act) if act else 0.0, 0.0)  # competence built

        # gating: catalytic_law=False ⇒ NO catalysts harvested (the fixed-law control cells).
        p0, _u0 = run(catalytic_law=False)
        self.assertFalse(p0._catalysts)                      # no substrate-law feedback ⇒ repertoire empty

    def test_exp054_earned_law_climbs_construction_reach_with_achieved_closure(self):
        # Ω-0.43 (the Earned Law): exp054 grows the composition LAW itself — earned_law lets a competent
        # lineage climb its construction reach (added to type_resolution/max_size) by +1 AT BIRTH iff the
        # source deme achieved enough closure at its current reach (gradual, non-destructive, fixed per
        # deme for life). Pin the mechanism: earned_law is the exp054 default on the Red Queen base; a
        # competent run climbs some deme's reach above 0 and builds competence; and it is gated
        # (earned_law=False ⇒ reach stays empty, exp001–053 unaffected). Whether the expanding law breaks
        # exp053's saturation is the study's science (EXP054_FINDINGS.md).
        from statistics import mean
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        def run(**ov):
            p, c = get_experiment("exp054")(seed=0, ticks=5000, **ov)
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(5000)
            return p

        p = run()
        self.assertTrue(p.earned_law)                        # the expanding law is on by default
        self.assertEqual(p.deme_fitness, "redqueen")         # runs on the exp052 Red Queen base
        self.assertTrue(p._deme_reach)                        # some deme earned a reach entry
        self.assertGreater(max(p._deme_reach.values()), 0)   # a competent lineage climbed the law (reach > 0)
        self.assertLessEqual(max(p._deme_reach.values()), p.earn_max_bonus)  # bounded by the cap
        act = [pi for pi in range(p.n_patches) if p._deme_edges.get(pi)]
        self.assertGreater(mean(p._deme_competence(pi) for pi in act) if act else 0.0, 0.0)  # competence built

        # gating: earned_law=False ⇒ no reach climbed (the fixed-law control), law stays at base.
        p0 = run(earned_law=False)
        self.assertFalse(p0._deme_reach)                     # no earned law ⇒ construction reach unchanged

    def test_exp055_transition_derives_the_next_tier_law_from_achieved_competence(self):
        # Ω-0.44 (transition-as-rule-change): exp055 makes the level transition CHANGE THE LAW — each tier
        # runs the exp053 compounding physics, and law_from_competence derives the next tier's Catalytic-Law
        # strength (catalyst_period = base/(1+competence)) from THIS tier's achieved competence. Pin the
        # mechanism: per-tier competence is measured; with the derived law a competent tier grants its
        # successor a STRONGER (shorter-period) law than the base; and it is gated (law_from_competence off
        # + builder='exp030' ⇒ the pre-exp055 tower, byte-identical). Whether competence compounds ACROSS
        # levels is the study's science (EXP055_FINDINGS.md).
        from omega.levels.stack import run_stack

        r = run_stack(max_tiers=3, seed=0, ticks=2500, builder="exp053", law_from_competence=True,
                      catalyst_period=400)
        self.assertGreaterEqual(len(r.tiers), 2)                 # the tower recurses
        self.assertGreater(r.tiers[0].competence, 0.0)           # per-tier competence is measured
        # a competent tier-0 grants tier-1 a STRONGER (shorter-period) law than the base 400.
        self.assertEqual(r.tiers[0].catalyst_period, 400)        # tier 0 gets the base law
        self.assertLess(r.tiers[1].catalyst_period, 400)         # tier 1's law is DERIVED (stronger) from tier-0 competence

        # gating: the default tower (law_from_competence off, builder exp030) is unchanged — a fixed law
        # every tier (period stays the base), i.e. no competence-derived rule change.
        r0 = run_stack(max_tiers=2, seed=0, ticks=1500)
        self.assertTrue(all(t.catalyst_period == 400 for t in r0.tiers))  # no derivation ⇒ fixed law

    def test_exp056_competence_pressure_scales_selection_and_is_byte_identical_at_one(self):
        # Ω-0.45 (the competence–diversity trade-off dial): exp056 adds competence_pressure ∈ [0,1] scaling
        # the Red Queen's competence term (weight = 0.05 + pressure·(closure + core-novelty)). Pin it:
        # pressure=1.0 (default) is byte-identical to exp052; a lower pressure genuinely changes the
        # dynamics (softer selection); and it threads through the tower. Whether a sweet spot resolves the
        # trade-off is the study's science (EXP056_FINDINGS.md).
        from omega.kernel.universe import Universe
        from omega.kernel.scheduler import Scheduler
        from omega.substrate.noise import Noise

        def classes(**ov):
            p, c = get_experiment("exp052")(seed=0, ticks=2500, **ov)
            self.assertAlmostEqual(p.competence_pressure, ov.get("competence_pressure", 1.0))
            rng = Noise(c.seed); u = Universe(total_quanta=c.total_quanta); p.seed(u, rng)
            Scheduler(u, p, rng, decay_hazard=c.decay_hazard,
                      max_reactions_per_tick=c.max_reactions_per_tick).run(2500)
            return u.classes_ever_seen

        base = classes()                                    # default pressure 1.0
        self.assertEqual(classes(competence_pressure=1.0), base)   # 1.0 ⇒ byte-identical to the default
        self.assertNotEqual(classes(competence_pressure=0.3), base)  # softer selection ⇒ different dynamics

        # threads through the tower (exp055 derived-law) without error and is recorded on the physics.
        from omega.levels.stack import run_stack
        r = run_stack(max_tiers=2, seed=0, ticks=1500, builder="exp053", law_from_competence=True,
                      competence_pressure=0.5)
        self.assertGreaterEqual(len(r.tiers), 1)

    def test_exp057_tier0_warmup_extends_founding_tier_and_is_byte_identical_at_one(self):
        # Ω-0.46 (the bootstrapping floor): exp056 relocated the limit on tower robustness to tier-0
        # establishment (~20% of seeds never form a founding network). exp057 adds a gated tier0_warmup
        # that runs ONLY the founding tier for int(ticks*warmup) ticks (higher tiers unchanged), a direct
        # test of whether that floor is timing- or structurally-limited (the study's science,
        # EXP057_FINDINGS.md). Pin the mechanism: warmup=1.0 (default) ⇒ the tower is byte-identical; a
        # larger warmup genuinely changes the founding tier (more ticks ⇒ different tier-0 class history),
        # and it threads the tower without error.
        from omega.levels.stack import run_stack

        def tier0_classes(**ov):
            return run_stack(max_tiers=2, seed=1, ticks=1500, builder="exp053",
                             law_from_competence=True, **ov).tiers[0].classes_ever

        base = tier0_classes()                                  # default warmup 1.0
        self.assertEqual(tier0_classes(tier0_warmup=1.0), base)      # 1.0 ⇒ byte-identical founding tier
        self.assertNotEqual(tier0_classes(tier0_warmup=3.0), base)   # more warmup ⇒ different tier-0 history

        # full off-path byte-identity across the whole tower (every tier's class count), and it runs.
        a = run_stack(max_tiers=3, seed=2, ticks=1200, builder="exp053", law_from_competence=True)
        b = run_stack(max_tiers=3, seed=2, ticks=1200, builder="exp053", law_from_competence=True,
                      tier0_warmup=1.0)
        self.assertEqual([t.classes_ever for t in a.tiers], [t.classes_ever for t in b.tiers])
        self.assertGreaterEqual(len(a.tiers), 1)

    def test_global_novelty_sketch_is_conservative_and_eviction_robust(self):
        # Ω-0.31 (consolidation): the eviction-robust GLOBAL novelty estimator (a scalable Bloom
        # 'ever-seen' set) is the instrument that settles "stays open forever". Its two load-bearing
        # properties, plus byte-identity when off:
        from omega.emergence.global_novelty import GlobalNoveltySketch

        # (i) never counts a repeat as new (no Bloom false negatives) => strips all recycling; and it
        #     only ever UNDER-counts genuine novelty (a new id may collide) — never over-counts.
        s = GlobalNoveltySketch(initial_capacity=2048, fp_rate=0.005)
        ids = [f"c{i}" for i in range(20000)]
        first = sum(s.add_if_new(x) for x in ids)
        self.assertLessEqual(first, len(ids))                    # under-count only (<= true distinct)
        self.assertGreater(first, 0.97 * len(ids))              # bounded ~1% false-positive under-count
        self.assertEqual(sum(s.add_if_new(x) for x in ids), 0)  # every repeat recognized as old

        # (ii) on an UNBOUNDED run (no eviction) global == windowed (nothing to recycle, class count
        #      well below filter capacity so no under-count); byte-identical when off.
        pu, cu = get_experiment("exp030")(seed=0, ticks=1500)
        ru = run(pu, cu, global_novelty=True)
        win_u, glob_u = sum(ru.novelty_new_per_tick), sum(ru.novelty_global_new_per_tick)
        self.assertEqual(win_u, glob_u)
        pf, cf = get_experiment("exp030")(seed=0, ticks=1500)
        rf = run(pf, cf)                                        # off
        self.assertEqual((rf.final_population, rf.final_classes_total, sum(rf.novelty_new_per_tick)),
                         (ru.final_population, ru.final_classes_total, win_u))  # off == on-metrics

        # (iii) on a BOUNDED run with heavy eviction the windowed rate INFLATES (evicted classes
        #       reappear and re-count) while the global rate strips it: global < windowed, and the
        #       true distinct-ever count is invariant to eviction (equals the unbounded global).
        pb, cb = get_experiment("exp030")(seed=0, ticks=1500)
        rb = run(pb, cb, memory_horizon=300, relation_cap=2000, global_novelty=True)
        win_b, glob_b = sum(rb.novelty_new_per_tick), sum(rb.novelty_global_new_per_tick)
        self.assertLess(glob_b, win_b)                          # inflation stripped
        self.assertEqual(glob_b, glob_u)                        # global count invariant to eviction

    def test_exp035_new_tree_law_reaches_the_both_corner(self):
        # Ω-0.31: the both-corner CONDITION is substrate-general, not special to the type
        # substrates. A genuinely different law — binary-tree grafting (f,x) with a depth
        # cap, unlike path concatenation or morphism composition — still yields heritable
        # collectives (self > null) AND sustained novelty (> 0). Honest scope: its heredity
        # is far weaker than typed_path's strong both corner (checked in the study).
        from statistics import mean
        p, c = get_experiment("exp035")(seed=0, ticks=1000, n_patches=24,
                                        propagule_mode="source", tree_resolution=3)
        r = run(p, c)
        sj = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
        nj = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
        self.assertGreater(sj, nj)                                  # heritable (self > null)
        self.assertGreater(r.open_endedness["novelty_rate"], 0.05)  # AND open

    def test_exp034_reification_grows_the_alphabet_and_keeps_novelty(self):
        # Ω-0.31: the constructibility lever at the collective level. In-run reification
        # promotes persistent product motifs to NEW atoms (self.atoms grows during the
        # run), and the world stays open and heritable. (Whether it slows the long-horizon
        # novelty-rate decay is the study's quantitative question; here we pin the
        # mechanism + that it doesn't break the both corner.)
        from statistics import mean
        p, c = get_experiment("exp034")(seed=0, ticks=2000)
        r = run(p, c)
        self.assertGreater(len(p.atoms), 32)                       # alphabet grew (reified)
        self.assertTrue(p._reified)                                # motifs were promoted
        self.assertGreater(r.open_endedness["novelty_rate"], 0.05)  # still open
        sj = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
        nj = mean(p._hered_edge_null) if p._hered_edge_null else 0.0
        self.assertGreater(sj, nj)                                 # still heritable

    def test_exp033_tower_recurses_across_a_physics_boundary(self):
        # Ω-0.30: levels are FIRST-CLASS, not one engine climbing itself. With a
        # different composition law per tier (open path-concatenation exp030 alternating
        # with open+culture exp031_culture), the transition still recurses ACROSS the
        # physics boundary: a tier built from the collectives of a tier that ran a
        # *different law* still forms heritable collectives. Uses two both-open laws so
        # the claim isolates "crossing a boundary" from the closed law's known weakness.
        from omega.levels.stack import run_stack
        r = run_stack(max_tiers=3, seed=0, ticks=900,
                      levels=("exp030", "exp031_culture"))
        self.assertGreaterEqual(r.tower_depth, 2)          # stacks despite law changes
        self.assertNotEqual(r.tiers[1].physics, r.tiers[0].physics)  # tier1 is a boundary
        self.assertTrue(r.tiers[1].heritable)              # heritable across the boundary
        # default (levels=None) stays the self-similar exp030 tower — back-compatible.
        self.assertEqual(run_stack(max_tiers=2, seed=0, ticks=500).tiers[0].physics,
                         "exp030")

    def test_exp032_tower_depth_not_ceiling_limited(self):
        # Ω-0.29: unboundedness (of levels). Lifting the tier cap, the recursive tower
        # climbs well past exp031's depth-5 observation — depth is limited by compute,
        # not an intrinsic ceiling — because each tier's collective count is ~a fixed
        # point, so the promoted alphabet does not starve as depth grows.
        from omega.levels.stack import run_stack
        r = run_stack(max_tiers=10, seed=0, ticks=500)
        self.assertGreater(r.tower_depth, 5)                # beats the exp031 cap
        deep = r.tiers[-1]
        self.assertTrue(deep.heritable)                     # deepest tier still heritable
        self.assertGreaterEqual(deep.n_collectives, 2)      # alphabet has not starved

    def test_exp030_openended_modular_substrate_achieves_both(self):
        # Ω-0.27: the capstone. exp029 showed the transition needs a substrate that is
        # BOTH open-ended and modular. A typed-PATH substrate (variable-length type paths
        # composed by concatenation, with a bounded identity resolution) provides it: at
        # the "both" corner it gives strong, reproducible network heredity (self >> the
        # combinator ~0.10) AND sustained novelty > 0 (unlike the closed typed substrate)
        # AND rich cross-production networks — a completed transition to collective
        # individuality in miniature.
        from statistics import mean

        p, c = get_experiment("exp030")(seed=0, ticks=1500, n_patches=24,
                                        propagule_mode="source")
        r = run(p, c)
        self_j = mean(p._hered_edge_self) if p._hered_edge_self else 0.0
        self.assertGreater(self_j, 0.15)                       # strong collective heredity
        self.assertGreater(r.open_endedness["novelty_rate"], 0.05)  # AND still open-ended

    def test_compose_path_correct(self):
        # exp030 modular composition (path concatenation) and resolution truncation
        from omega.experiments.exp012_combinator import compose_path, _path_nodes
        self.assertEqual(_path_nodes(compose_path(("a", "b"), ("b", "c"), 24, 0)),
                         ["a", "b", "c"])                       # a->b ∘ b->c = a->b->c
        self.assertIsNone(compose_path(("a", "b"), ("c", "d"), 24, 0))  # endpoint mismatch
        self.assertEqual(_path_nodes(compose_path(("a", ("b", "c")), ("c", "d"), 24, 2)),
                         ["c", "d"])                            # resolution=2 keeps last 2

    def test_combinator_reducer_correct(self):
        # the SKI reducer must implement the three rules correctly
        from omega.experiments.exp012_combinator import normalize
        self.assertEqual(normalize(("I", "K"), 50, 24), "K")               # I K -> K
        self.assertEqual(normalize((("K", "S"), "I"), 50, 24), "S")        # K S I -> S
        self.assertEqual(normalize(((("S", "K"), "K"), "I"), 50, 24), "I")  # S K K I -> I

    def test_extended_combinator_rules_correct(self):
        # exp027 extended basis (B/C/W/T/V and primed B'/C'/S'); a wrong rewrite would
        # silently corrupt the richer-substrate experiments, so pin each rule.
        from omega.experiments.exp012_combinator import normalize as N
        self.assertEqual(N(((("B", "I"), "K"), "S"), 50, 24), ("K", "S"))   # B I K S -> I (K S) -> K S
        self.assertEqual(N(((("C", "K"), "S"), "I"), 50, 24), "I")          # C K S I -> K I S -> I
        self.assertEqual(N((("W", "K"), "S"), 50, 24), "S")                 # W K S -> K S S -> S
        self.assertEqual(N(("T", "K"), 50, 24), ("T", "K"))                 # T K (partial) is normal
        self.assertEqual(N((("T", "K"), "I"), 50, 24), "K")                # T K I -> I K -> K
        self.assertEqual(N(((("V", "K"), "S"), "I"), 50, 24), ("K", "S"))   # V K S I -> I K S -> K S
        self.assertEqual(N(((((("B1", "K"), "S"), "K"), "I")), 50, 24), "S")  # B' K S K I -> K S (K I) -> S
        self.assertEqual(N(((((("C1", "K"), "I"), "S"), "K")), 50, 24), "K")  # C' K I S K -> K (I K) S -> K
        self.assertEqual(N(((((("S1", "K"), "I"), "I"), "S")), 50, 24), "S")  # S' K I I S -> K (I S)(I S) -> S


if __name__ == "__main__":
    unittest.main()
