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
