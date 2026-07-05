# exp022 — Can a group-selectable trait *emerge* instead of being imposed?

This is the open problem exp021 left. exp021 showed the multi-level machinery works,
but its group trait was an **imposed** coop bit. exp017–020 showed nothing
group-selectable *emerges* from the combinator dynamics, because everything that
varied between demes was individual-level ("the best individual wins everywhere").
The missing element is **complementarity** — a property no single class can carry.

**Hypothesis.** An emergent group phenotype = membership in a *cross-producing
network*. Define a deme's fitness as its internal **cross-production**: reactions
where a member produces a *different* member (a class making another class already
present in the deme). This is irreducibly collective — a monoculture self-catalyst
scores ~0 (it only makes itself); only a mutualistic/autocatalytic set scores high,
and no single replicator can maximize it. No copy channel, no imposed bit — the
"cooperation" is emergent membership in the network. Registered as `exp022`
(`deme_fitness="network"`; gated, exp012–021 byte-identical, determinism preserved,
25/25 tests pass). Reproduce with `studies/exp022_*.py`.

**Novel, falsifiable prediction (opposite of exp021).** exp021's single-locus
cooperation needed *small* propagules (high relatedness on one locus). A multi-member
collective can only be inherited if the propagule carries enough of the network — so
here there should be a *transmission threshold*: the collective advantage should be
absent for tiny propagules and rise with propagule size (to an intermediate optimum).

## Result: yes — an emergent trait is both heritable and selectable at the group level

### Propagule-size sweep, `source` vs the well-mixed `mixed` null (4000 ticks, 5 seeds)

| propagule | source xprod | mixed xprod | source/mixed |
|----------:|:------------:|:-----------:|:------------:|
| 2  | 6.55 | 6.64 | **0.99** (transmission fails) |
| 4  | 6.92 | 6.51 | 1.06 |
| 8  | 7.00 | 5.94 | 1.18 |
| 16 | 6.94 | 5.63 | 1.23 |
| 24 | 6.94 | 4.72 | **1.47** |
| 40 | 6.94 | 4.70 | 1.48 |
| 60 | 6.94 | 5.23 | 1.33 |

The prediction holds. At propagule 2 the collective advantage is absent
(source ≈ mixed) — the network cannot be transmitted. As the propagule grows the
advantage climbs to a peak of ~1.48× at 24–40, then declines at 60 (bottleneck too
weak) — an **intermediate optimum**, exactly opposite to exp021's single-locus trait.
Notice the mechanism in the numbers: `source` cross-production is flat at ~6.9
regardless of propagule size (it always transmits its own deme's network), while
`mixed` *falls* as the propagule grows (a larger well-mixed draw scrambles more
structure). The collective advantage is the gap that opens between them.

### Decomposition: selection vs preservation (measure cross-production, select neutrally)

Is the `source` advantage genuine *selection for* the trait, or just `source`
*preserving* structure that `mixed` scrambles? A third arm — `source` propagules but
demes chosen by **size** (preserves structure, selects neutrally) — separates them:

| propagule | source-network | source-size | mixed |
|----------:|:--------------:|:-----------:|:-----:|
| 16 | 6.94 | 6.49 | 5.63 |
| 24 | 6.94 | 6.49 | 4.72 |

Both components are real and collective:

- **Collective heredity (preservation):** source-size − mixed = +0.86 (ps 16) →
  +1.77 (ps 24). Merely preserving a deme's composition maintains more
  cross-production, and this grows with propagule size — the transmission threshold
  lives here.
- **Collective selection:** source-network − source-size = +0.45 at both sizes.
  Additionally selecting cross-productive demes to reproduce adds a further boost
  that size-selection does not — genuine group-level selection *for* the emergent
  trait, on top of heredity.

## Interpretation — a qualified "yes" to the open problem

A group-selectable trait **can** emerge from the substrate's own dynamics: internal
cross-production is an emergent, heritable, selectable collective property, and both
collective heredity and collective selection demonstrably act on it, with the
predicted transmission-threshold signature that distinguishes a multi-member
collective from a single-locus one.

Two honest caveats keep this modest, not a full major transition:

1. **No individuation.** `n_deme_types` stays ~19/24 in both arms — demes do *not*
   converge on one shared collective type. Each deme independently maintains its own
   cross-producing network; between-deme diversity is preserved. Collective selection
   improves the *quality* of demes without homogenizing them.
2. **Bounded magnitude.** The advantage is ~1.5× and cross-production is ~7
   events/deme — a functional collective structure, not a dominant one. As in exp021,
   collective selection here is a real but bounded force.

So the arc's verdict sharpens: collectives do not *spontaneously* outcompete
individuals (exp017–020), but the substrate *does* admit emergent, group-selectable
collective structure once fitness is defined on an irreducibly collective property
(exp022) — and, given such a trait, multi-level selection behaves as theory predicts
(exp021/exp022). What is still missing for a true major transition is *individuation*:
demes becoming discrete, competing collective individuals rather than independently
well-structured containers.

## Remaining open problems and speculative next hypotheses

The exploration leaves a concrete agenda for getting from "group-selectable
structure" to "collective individuals":

- **H-A · Niche construction / stigmergy as heredity.** Recycle a deme's own recent
  products as its local feed instead of random feed. A deme's environment becomes
  part of its heritable phenotype, a second inheritance channel that could raise
  within-deme dominance (the wall of exp017–020) and let networks self-reinforce.
- **H-B · Reproductive division of labor (germ–soma).** Let some classes be
  high-cross-production but low-replication ("soma") while reproduction flows through
  a transmitted "germ" subset. This is the Volvox route to individuality and directly
  attacks within-deme conflict, which currently erodes every collective.
- **H-C · Obligate networks via co-transmission.** Combine exp016's knockout-obligate
  hypercycles with exp022's network fitness: select demes whose members are
  *mutually dependent* (removing one collapses production), so the collective, not
  the parts, is the only viable unit — the condition for genuine individuation.
- **H-D · Conflict mediation / policing.** Add a within-deme mechanism that
  suppresses fast selfish replicators (a random bottleneck, or a cost on defection),
  realigning within- and between-deme fitness so cooperation need not rely on extreme
  relatedness (relaxing exp021's constraint).

The single most promising is **H-A**: it is a different *inheritance* mechanism
(environmental, not just propagule), and it targets the one wall — the absence of
within-deme dominance — that blocked exp017–020 and still caps exp022's networks.

---

**Follow-up (see `EXP023_FINDINGS.md`).** exp023 built H-A (niche construction:
recycle a deme's own products as its feed). It is the first lever to actually move
within-deme dominance (0.245 → 0.322) — confirming environmental heredity is a real
second channel — but it raises dominance *globally without differentiation*
(source ≈ mixed, no individuation) and halves the novelty rate. It amplifies shared
global winners in every deme rather than differentiating them, exposing a
chicken-and-egg: recycling locks in composition only once demes have diverged. The
conclusion is that no single lever suffices; exp021 (selection), exp022 (emergent
trait), and exp023 (within-deme dominance) each supply *part* of a transition, and
the next step is to **combine** them (e.g. recycle feed + network fitness + forced
founder divergence).
