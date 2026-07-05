# exp024 — Combining every lever: is collective individuation reachable, and if not, why?

exp021–023 each supplied *part* of a major transition but none individuated demes.
exp023's diagnosis was that its levers act globally, and the missing ingredient is
**forced founder divergence**. exp024 combines all of it and adds that ingredient —
then, when it still fails, localizes *why* to a new substrate-level wall.

**Mechanism (gated; exp012–023 byte-identical; determinism preserved; 27/27 tests
pass).** `exp024` = `feed_mode="recycle"` (exp023 within-deme dominance) +
`deme_fitness="network"` (exp022 collective selection) + `founder_mode="monoculture"`
(each deme seeded as a distinct monoculture — forced divergence) + `mig_rate=0`
(isolation). Reproduce with `studies/exp024_*.py`.

## Result: combining the levers does not individuate demes

Source vs mixed, exp023 vs exp024, 4000 ticks, 5 seeds:

| exp | mode | within-deme dom | heredity self/null | n_deme_types @t0 | n_deme_types late |
|-----|------|:---------------:|:------------------:|:----------------:|:-----------------:|
| exp023 | source | 0.328 | 1.59 | 12.6 | 14.9 |
| exp023 | mixed  | 0.319 | —    | 12.6 | 15.6 |
| exp024 | source | 0.330 | 1.40 | 12.8 | 15.4 |
| exp024 | mixed  | 0.323 | —    | 12.8 | 14.9 |

Adding network fitness and monoculture founding on top of recycle changes **nothing**:
within-deme dominance is identical (0.330 vs 0.328), collective heredity is if
anything slightly *lower* (1.40 vs 1.59), and there is no individuation — exp024
`source` vs `mixed` late `n_deme_types` differ only by noise (seed-level diffs +4.3
and −3.1 across seeds; mean ~flat). The combination is inert.

## The diagnosis: a new substrate-level wall — type-space poverty

The decisive clue is `n_deme_types` **at tick 0 = ~13**, even though 24 patches were
each seeded as a *distinct* monoculture. Twenty-four supposedly-distinct founders
**collide onto ~a dozen classes** before a single reaction has fired. Measuring the
feed's own type distribution (5000 draws) shows why:

- 204 distinct normal forms exist, **but the top 3 carry ~43% of the mass and the
  top 9 carry ~72%.** Small combinator expressions reduce to a handful of common
  **attractor** normal forms.

So there simply are not enough *distinct, common, stable* types to give 24 demes
distinct persistent identities. Whatever a deme is founded on, it is quickly invaded
by the shared global attractors (the ~9 common forms), which are common precisely
because they are attractors of the reduction dynamics — and recycling, isolation, and
collective selection cannot manufacture identities the substrate does not offer. The
individuation barrier is **not** the multi-level machinery (exp021/022 proved that
works); it is that the SKI substrate's small-expression normal-form space is too
shallow to support many distinct collective phenotypes.

## Significance — an echo of the Phase-A → Phase-B pivot

This is the same *kind* of wall the program hit before. exp009–011 showed a
form-based substrate could not support function/reproduction — a substrate ceiling,
not a mechanism bug — which forced the Ω-0.9 pivot to the behaviour-first SKI soup.
exp017–024 now show the SKI soup supports individual open-ended evolution, ecology,
obligate collectives, and working multi-level selection *on a supplied trait* — but
its **type space is too poor to individuate collectives**: ~9 attractor types cannot
seed 24 distinct heritable demes.

**Where this points (a substrate pivot, not another knob).** The evidence across
exp017–024 is consistent: the multi-level machinery is sound; what is missing is a
substrate offering **many distinct, stable, heritable collective phenotypes**. Candidate
next substrates, in the spirit of the Ω-0.9 pivot:

- **Larger / typed combinators or lambda terms** — a normal-form space with a broad,
  flat distribution of stable types (not ~9 attractors), so demes can hold distinct
  identities. The direct test: does the same exp024 machinery individuate once the
  feed's type distribution has, say, >50 roughly-equifrequent stable forms?
- **Compositional deme phenotypes** — make a deme's identity a *combination* of member
  types (a network signature) rather than a single dominant class, so identity space
  is combinatorial (rich) even if the per-member type space is small. This reframes
  individuation around exp022's cross-production networks as the unit of heredity,
  and is implementable within the current substrate — the most promising next step
  that does *not* require a full pivot.

## Status of the collective-individuation problem after exp017–024

- **Multi-level selection works** given a heritable group trait (exp021 imposed,
  exp022 emergent) — the machinery is not the bottleneck.
- **Within-deme dominance** can be lifted by environmental heredity (exp023) but not
  past ~0.33, and not into distinct demes.
- **Full individuation is blocked** by substrate type-space poverty (exp024): too few
  stable attractor types to give many demes distinct heritable identities.

The honest verdict: a *complete* major transition to collective individuality is not
reachable in the small-expression SKI substrate. The next real move is a richer type
space — either a substrate pivot, or (cheaper, and testable now) redefining deme
identity combinatorially over cross-production networks so that a small per-member
type space still yields many distinct collective phenotypes.
