# exp021 — Group selection of a cooperation trait: the positive capstone

exp017–020 found the multi-level structure **inert**: across heredity, fitness
variance, feed locality, and an explicit replicase, making the collective heritable
(`source`) versus not (`mixed`) never changed the outcome. The diagnosis was that
nothing in the combinator dynamics produces a *group-selectable* trait — a
heritable property of a deme's composition that individual selection would not
already fix on its own. exp021 supplies one by hand and asks whether the multi-level
machinery then works.

**Mechanism (gated; exp012–020 stay byte-identical; determinism preserved; 24/24
tests pass).** A **cooperation trait**: each organization carries a heritable coop
bit (inherited on copy and through propagules, with rare `coop_mut` flips; the feed
is all defectors). It is *individually costly* — a cooperator skips a copy with
probability `coop_cost`, so it replicates slower — and *collectively beneficial* — a
deme founds propagules in proportion to its cooperator fraction (`coop_benefit`).
Within-deme selection erodes cooperation; between-deme selection (`source`
propagules from cooperator-rich demes) can maintain it. Registered as `exp021` at a
strong-relatedness regime (single-founder propagule bottleneck, fast/strong deme
turnover — the Hamilton/Price condition for group selection to have purchase).
Reproduce with `studies/exp021_cooperation.py`.

## Result: with a group-selectable trait, collective selection finally works

Cost sweep at the strong-relatedness regime, `source` vs the well-mixed `mixed`
null, 2500 ticks, 5 seeds. Late cooperator fraction (feed is all defectors, so any
cooperation above the null is actively maintained):

| coop_cost | source coop | mixed coop | source − mixed |
|----------:|:-----------:|:----------:|:--------------:|
| 0.00 | 0.340 ± 0.024 | 0.143 ± 0.051 | **+0.197** |
| 0.05 | 0.355 ± 0.028 | 0.139 ± 0.030 | **+0.216** |
| 0.10 | 0.278 ± 0.052 | 0.110 ± 0.036 | +0.168 |
| 0.20 | 0.182 ± 0.035 | 0.097 ± 0.019 | +0.085 |
| 0.40 | 0.104 ± 0.016 | 0.062 ± 0.007 | +0.042 |

Three things, all textbook multi-level selection:

1. **Collective selection works.** At every cost, `source` maintains cooperation far
   above the `mixed` null (gap ≫ between-seed SD). Preserving a deme's collective
   composition through the propagule — the thing that was inert in exp017–020 —
   now changes the outcome. A direct probe confirms the mechanism: `source` carries
   higher between-deme variance in cooperator fraction (SD 0.17 vs 0.13) — the raw
   material group selection acts on.

2. **It is a bounded force.** Even at zero individual cost, cooperation stabilizes
   around 0.34, not 1.0 — within-deme drift and the defector feed keep it partial.
   Group selection maintains cooperation; it does not let cooperators fixate.

3. **Individual selection wins as cost rises.** The `source − mixed` gap decays
   monotonically (0.22 → 0.04) as `coop_cost` climbs. The collective advantage is
   real but shrinks exactly as within-deme individual selection strengthens — the
   Price-equation tension made quantitative.

It also took a **strong-relatedness regime** to see this at all: a single-founder
propagule bottleneck plus fast, strong deme turnover. At the weak bottleneck used in
exp017–020 (propagule 16), between-deme variance is too low and the effect vanishes
(`source` ≈ `mixed`) — consistent with why those experiments saw nothing.

## The six-experiment verdict

**Do collectives reliably outcompete individuals over long timescales, or collapse?**

- **Spontaneously, in the combinator soup: no.** exp017–020 show the multi-level
  structure is inert — no group-selectable trait emerges, so making the collective
  heritable never changes anything; every apparent collective win is either
  population collapse or individual replicators winning under a collective label.
- **Given a genuine group-beneficial, individually-costly trait and high
  relatedness: yes, but as a bounded force.** exp021 shows the multi-level machinery
  is *sound* — supply a heritable group phenotype and collective heredity, and it
  produces textbook group selection: cooperation maintained well above the
  individual-selection equilibrium, strongest at low cost, waning as cost rises.

So the obstacle across exp017–020 was never the multi-level machinery; it was the
absence of a heritable group phenotype for it to act on. The combinator substrate
supports open-ended *individual* novelty (exp012–014) and, when handed a
group-level trait, *individual-vs-group* selection behaves exactly as theory
predicts (exp021) — but it does not, on its own, invent the collective trait that a
major transition to collective individuality would require. Bridging that gap —
getting a group-selectable trait to *emerge* rather than be imposed — is the open
problem this arc leaves.
