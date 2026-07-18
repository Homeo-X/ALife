# exp048 — The loop-back: part-level replicators lift the competence *ceiling* (~2×) but do not close the *compounding* gap

exp047 closed the self-improvement arc with a terminal diagnosis: collective competence is irreducibly
collective, and the typed_path substrate's parts are context-dependent network components, not
replicators — so no selection route makes competence compound. exp012 found the one place genuine
**part-level replicators** emerge: the behaviour-first SKI-combinator soup, where an organization can
emit a copy of *itself* (`C·x → C`). exp048 runs the exp046 credit machinery on that substrate and
closes the loop from the arc's end back to its beginning.

## Mechanism (gated substrate override, default off ⇒ exp001–047 byte-identical)

exp048 = the exp046 credit machinery (`deme_fitness="credit"` + heritable per-class credit map + the
exp040 heredity channel) with `substrate="combinator"` — so a credited part can carry and copy its
*own* heritable value (a replicator), rather than being a context-dependent path fragment. Arms:
`replicator` (combinator + credit), `network` (typed_path + credit — exactly exp046), and
`replicator-drift` (combinator + `size` — isolates whether credit adds anything on the replicator
substrate).

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (mean, slope) | closure (mean) | distinct classes |
|-----|:---:|:---:|:---:|
| **replicator** (combinator + credit) | **1.088**, +0.001/win | **0.363** | 19,050 |
| network (typed_path + credit = exp046) | 0.635, −0.008/win | 0.130 | 3,283 |
| replicator-drift (combinator + size) | 0.934, +0.006/win | 0.315 | 23,171 |

**Verdict: a mixed result — replicators lift the *ceiling*, but competence still does not *compound*.**

- **Part-level replicators nearly double competence and triple closure.** On the combinator substrate
  collectives reach competence ~**1.09** (vs typed_path's 0.62) and closure ~**0.36** (vs 0.13), with
  ~6× more distinct classes — a large, robust *substrate* effect. exp047's diagnosis is **partially
  vindicated**: whether the parts are replicators matters a great deal for *how competent* the
  collectives become.
- **But competence is high-and-flat, not rising.** No arm compounds: replicator+credit slope +0.001
  (flat), replicator-drift +0.006 (barely rising), network −0.008 (declining). Competence plateaus at
  a substrate-dependent level; nothing makes it climb over generations. And credit selection is *not*
  the lever even here — it raises the plateau (1.09 vs drift 0.94) but flattens the slope.

## Interpretation — construction compounds; competence plateaus

The loop-back resolves the arc, but not the way a clean "yes" would. Replicating parts were the missing
ingredient for **high** collective competence (exp047 was right that the type-path parts' lack of
self-replication capped it), yet they are **not** sufficient for **compounding** competence — the
open-ended *rise* the whole self-improvement arc was chasing. On both substrates competence settles at
a ceiling and stays there.

This lands exactly on the program's own central distinction. Ω-0.31 established that **construction is
open-ended**: the genuine novelty rate stays positive — the world keeps building never-seen classes
forever (the combinator substrate here reaches ~19–23k distinct classes). But **competence is not
open-ended**: the collectives get *more competent up to a substrate-set ceiling* and then plateau, no
matter the selection or the parts' replicator status. Open-ended **novelty** ≠ open-ended
**competence**. The world compounds *what it builds*; it does not compound *how good its collectives
are*. Self-improvement-as-unbounded-competence-growth is **not** achieved in this substrate family —
and exp048 shows the obstacle is not merely "the parts aren't replicators" (fixing that lifts the
ceiling) but something deeper: nothing in the dynamics couples a collective's competence to an
*ever-rising* target once the substrate's ceiling is reached.

The full arc, one line each:
- **exp039–042** competence won't compound under scalar objectives → **goal representation** missing.
- **exp044** heritable, composable goals → transient deepening, no competence lift.
- **exp045/046** aim the goal at / put credit in the fitness → still no compounding → **selection grain**.
- **exp047** within-collective selection → **collapses** the collective → competence is irreducibly
  collective; the parts aren't replicators.
- **exp048** run it on the replicator substrate → competence ceiling **~2× higher**, but **still flat**
  → **part-level replicators lift the ceiling but do not make competence compound**: open-ended
  novelty is real, open-ended competence is not.

## Honest scope

Within-substrate measures; the combinator substrate's "both corner" is weak (the exp024–028 heredity
wall), so its collective heredity is lower even though its closure/competence *level* is higher —
another reason the level rises but the trajectory doesn't ratchet. The result is robust across 6 seeds
and 12k ticks (replicator ≫ network on competence and closure every window; all slopes ≈ 0). It does
**not** prove no substrate can compound competence — it shows the two substrates the program has
(type-path and combinator) both plateau, and that replicators raise the plateau without tilting it.

## Consequence — the arc rests, with a sharpened question

The self-improvement arc (exp036–048) is complete and honest: it separated **two kinds of
open-endedness** and showed this substrate family delivers one (novelty/construction) but not the
other (competence). The sharpened open question for any future attempt is no longer "represent the
goal / assign the credit / select the parts" — all ruled out — but **what dynamical coupling makes a
collective's competence itself a *rate* rather than a *stock***, the Ω-0.20 lesson applied to
competence instead of novelty. That is the real unsolved problem the arc isolates, and it is a
substrate/measurement question, not another selection knob.

## Reproduce
`PYTHONPATH=. python3 studies/exp048_replicator.py 12000 6 4000` → the table above; committed as
`studies/exp048_results.json` / `_console.txt`. Pinned by
`test_exp048_loopback_runs_credit_on_the_replicator_substrate` (credit machinery on the combinator
substrate builds a heritable credit map and a closure-forming network). Deterministic across
`PYTHONHASHSEED`; `deme_fitness` default ⇒ exp001–047 byte-identical.
