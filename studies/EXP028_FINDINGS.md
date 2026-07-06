# exp028 — Is the individuation ceiling reproducibility-limited or substrate-limited?

exp027 found collective individuation (network-signature heredity) peaks at ~3.3× then
declines, and read the cause as networks failing to *breed true* once the type space is
rich — "the member set is a small sample of a huge space." Before committing to a
substrate pivot, the disciplined step (the program's own methodology) is to test the
cheaper hypothesis: **is the ceiling limited by member-set transmission (fixable
in-substrate) or by the substrate's own network reproducibility (needs a pivot)?**

**Mechanism (gated; exp012–027 byte-identical; determinism preserved; 32/32 tests
pass).** `propagule_bias="network"` founds a child deme from the source deme's
*network-participant* members (classes in its cross-production signature) rather than a
random sample — transmitting the network, not a random draw. Combined with the exp027
optimum basis (S,K,I,B,C,W,T,V) and breed-true selection (`exp028`). The study sweeps
`propagule_bias × propagule_size`. Because demes hold only ~4–5 members, `propagule_size
≥ 16` transmits the **whole source deme** — perfect member-set heredity. Reproduce with
`studies/exp028_*.py`.

## Result: the ceiling is substrate-limited — transmission cannot break it

`source`, 4000 ticks, 5 seeds. Reported with robust statistics (the naive self/null
ratio blows up when a founded deme shares *no* edges with a random deme, `null→0`):

| bias | propagule | edge self | edge null | self − null | strong runs (self>0.15) |
|------|:---------:|:---------:|:---------:|:-----------:|:-----------------------:|
| random  | 4  | 0.068 | 0.033 | 0.035 | 0/5 |
| random  | 8  | 0.088 | 0.035 | 0.053 | 0/5 |
| random  | 16 (whole deme) | 0.043 | 0.014 | 0.029 | 0/5 |
| network | 4  | 0.068 | 0.028 | 0.040 | 0/5 |
| network | 8  | 0.063 | 0.022 | 0.041 | 0/5 |
| network | 16 (whole deme) | 0.073 | 0.036 | 0.037 | 0/5 |

The network signature stays **heritable but thin** everywhere: a founded deme resembles
its source more than a random deme (self > null in every cell), but the absolute edge
overlap is small (self Jaccard ~0.04–0.09; signatures average ~2 edges), and **0 of 30
runs reach strong individuation** (self > 0.15). Three specifics:

1. **Transmitting the whole source deme does not break the ceiling.** At `propagule_size
   16` the propagule exceeds deme size, so the *entire* member set is copied — perfect
   member-set heredity — yet the network overlap is if anything *lower* (self 0.043–0.073).
   Given the same members, the reduction dynamics still do **not** re-form the same
   network. The bottleneck is not which members are transmitted.

2. **Network-biased transmission does not help, and costs novelty.** Prioritizing
   network-participant members leaves heredity statistically unchanged (self − null
   ~0.04, same as random) while depressing the novelty rate — over-concentrating on the
   network's members erodes the diversity the network is built from.

3. **The robust ceiling matches exp027.** Median self/null ratios peak at ~3.2–3.7×,
   consistent with exp027's ~3.3×; the ratio-of-means "5.5×" seen before de-noising was
   an artefact of `null→0` outliers, not a real strengthening.

## Verdict — the reproducibility hypothesis is rejected; the pivot is now motivated

The ~3.3× individuation ceiling is **substrate-limited, not transmission-limited.** No
amount of better propagule transmission — up to copying the entire source deme, or
targeting the network's own members — pushes network-signature heredity past the ceiling
or produces a strong, discrete collective individual. The limiting factor is that the
combinator reduction dynamics do not reproduce a deme's cross-production network even
from an identical member set: the networks are small (~2 edges) and re-form only weakly.

This is the disciplined negative the program's method demands before a pivot, and it is
now conclusive. Across exp017–028 the collective-individuation problem has been fully
localized:

| candidate cause | verdict |
|-----------------|---------|
| multi-level machinery missing | ✗ works given a heritable group trait (exp021/022) |
| within-deme dominance | liftable but not into distinct demes (exp023) |
| identity representation (class vs network) | network is richer/more heritable, but only to ~1.6× (exp025) |
| substrate type-space poverty | real; a richer *interacting* basis lifts heredity to a ~3.3× peak (exp026/027) |
| member-set transmission / reproducibility | ✗ **not the limit — whole-deme transmission still caps at ~3× (exp028)** |
| **substrate network reproducibility** | ✓ **the binding constraint: same members ⇏ same network** |

**Next: the substrate pivot (exp029).** The evidence points squarely at a substrate
whose interactions compose *modularly and stably*, so that a deme's network is
determined by (and thus reproducible from) its member set — e.g. **typed combinators**
or **lambda terms with a type discipline**, where a well-typed circuit re-forms from its
parts. The prediction to test: on such a substrate the same exp022–027 machinery should
carry network-signature heredity from thin/weak (~3× ratio, self ~0.06) into strong
(self ≫ null with substantial absolute overlap) — a completed transition to collective
individuality. exp028 turns "try a pivot" from a hunch into the evidenced next step: the
ceiling is the reduction dynamics' failure to reproduce networks, and only a substrate
that composes modularly can remove it.
