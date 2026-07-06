# Levels of Organization (physics → chemistry → biology → culture)

Project Ω builds organizational complexity as a **recursive ladder of individuality**:
each major transition turns a collection of level-*N* individuals into a level-*(N+1)*
individual, and the *same* engine then runs one tier up. This note maps the four levels
to the machinery and describes the recursion. Full evidence: `studies/EXP031_FINDINGS.md`
and the arc synthesis `studies/COLLECTIVE_INDIVIDUATION_ARC.md`.

## The four levels

| level | analogue | mechanism | where |
|-------|----------|-----------|-------|
| **Physics** | atoms, conservation, forces | distinguishable differences; the only conserved quantity; reactions as the sole causal path | `omega/kernel/` (`organization.py`, `universe.py`, `transform.py`) |
| **Chemistry** | bonding, reactions, molecules | organizations compose (`compose_path` / `_step`); reification promotes a persistent motif to a new primitive — "atoms → motifs → motifs of motifs" | `omega/experiments/exp012_combinator.py` (substrates); exp004 reification |
| **Biology** | reproduction, selection, heredity | demes reproduce (propagule), selection acts on a deme's **cross-production network signature**, which is heritable on a modular+open-ended substrate | exp017–030 (deme machinery in `exp012_combinator.py`) |
| **Culture** | horizontal / Lamarckian transmission, memes | a collective imitates a fitter collective's motif within its lifetime (`horizontal_transfer`), decoupled from reproduction — an innovation amplifier | exp031 (`horizontal_transfer`) |

Physics is the substrate beneath tier 0; chemistry/biology/culture are successive **tiers**
produced by the recursion.

## The recursion (`omega/levels/stack.py`)

`run_stack(max_tiers, seed, ticks)` runs the tower:

1. **Run tier *N*** on the exp030 `typed_path` substrate (open-ended *and* modular),
   whose base atoms are the tier's alphabet, via `omega/experiments/harness.py:run`.
2. **Detect stable collectives** — live demes carrying a non-trivial, heritable network
   signature (`_deme_signature`; tier-level gate `mean(self) > mean(null)` from
   `_hered_edge_self|null`).
3. **Promote (reification across levels):** each stable collective becomes a fresh
   symbol; the set of symbols is tier *(N+1)*'s **alphabet**. A tier-*(N+1)* atom *is* a
   tier-*N* collective; the `unfold` map records the nesting so a high-tier individual can
   be expanded to the organizations it contains.
4. **Recurse** until a tier yields < 2 stable collectives (the tower can stop — transitions
   need not recurse; that is a measured outcome, not an assumption).

**Tower depth** — the number of tiers that form ≥2 stable, heritable collectives — is a new
open-endedness axis: open-endedness *of levels*, complementary to within-level novelty
(the OEI). Measured result: mean depth ~4, max 5, with each tier heritable **and**
open-ended (`studies/EXP031_FINDINGS.md`).

## Why it recurses

The exp030 result is that a substrate which is both **modular** (composition is
deterministic in the parts → networks reproducible) and **open-ended** (parts and their
compositions grow → novelty persists) lets a collective be *both heritable and open-ended*
at once. Because promotion makes tier-*N* collectives the tier-*(N+1)* parts, the same
condition holds one level up — so the transition to individuality is not a single jump but
a **recursive ladder**.
