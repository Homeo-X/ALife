# exp049 — Competence as a *rate*, not a *stock*: reifying achieved competence does **not** raise the ceiling (the arc's open problem, closed)

exp048 left the self-improvement arc with a single sharpened question. The program had *two* kinds of
open-endedness and had shown only one. **Construction is open-ended** (Ω-0.31: the genuine novelty rate
stays positive — the world keeps building never-seen classes forever). **Competence is not** (exp048:
collectives get more competent up to a substrate-set ceiling and then plateau, under every selection
route and on both substrates). The program's *answer* to plateauing **novelty** was Ω-0.20: openness is
a **rate**, sustained only by **continuing reification** — promoting achieved structure to new
primitives keeps the construction space growing. exp049 asks the obvious next question: does that same
lever, aimed at **competence**, make competence a rate too?

## Mechanism (gated, default off ⇒ exp001–048 byte-identical)

exp049 reuses the Ω-0.20/exp034 reification machinery but changes **what** gets promoted. `reify_by`
selects the ranking:

- **`reify_by="closure"` (exp049 treatment):** every generation, tally how often each class sits in a
  deme's **autocatalytic closure core** (`producers ∩ products` of the cross-production network —
  achieved *competent* structure). Every `reify_period` ticks, promote the **most closure-central**
  module to a new atom (`self.atoms`). Each cohort of collectives then builds on the previous cohort's
  competent modules — the competence *ceiling* itself might climb.
- **`reify_by="frequency"` (control):** the plain exp034 rule — promote the most *common* recent
  product (competent or not).
- **`reify_period=0` (control):** no reification at all — the exp048 plateau.

The tally is identity-only (no RNG); `reify_by`/`reify_period` off ⇒ exp001–048 byte-identical,
deterministic across `PYTHONHASHSEED`. Runs the exp030 both-corner base with closure selection.

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (mean, slope) | closure (mean) | final atoms | distinct classes |
|-----|:---:|:---:|:---:|:---:|
| **reify-closure** (reify competent structure) | 0.684, **+0.0006/win** | 0.199 | 51 | 5,796 |
| reify-freq (reify common structure, exp034) | 0.686, +0.0022/win | 0.201 | 53 | 5,870 |
| no-reify (the exp048 plateau) | 0.673, +0.0046/win | 0.193 | 32 | 4,594 |

**Verdict: competence stays a *stock*. Reifying achieved competence does not make competence compound.**

- **All three arms are flat.** Every slope is ≈ 0 (+0.0006, +0.0022, +0.0046 per window — the *no-reify*
  arm is nominally the *steepest*, all three are noise around zero). Competence oscillates in a fixed
  band ~0.63–0.80 in every arm across all 8 windows; the ceiling does not climb.
- **Reifying competent structure is no better than reifying common structure — or than not reifying.**
  Closure-keying (0.684) is statistically indistinguishable from frequency-keying (0.686) and from
  no-reification (0.673). *Which* module you promote is moot because promoting *any* module doesn't
  lift competence.
- **The constructed alphabet grows while competence doesn't.** The reify arms grow their atom set
  32 → 51–53 and discover ~26% more distinct classes than no-reify (5.8k vs 4.6k) — **novelty
  compounds** — yet competence stays flat. This is Ω-0.31's *open-ended novelty ≠ open-ended
  competence*, demonstrated **within a single experiment**: the very same reification that grows the
  construction space (novelty) leaves the competence ceiling untouched.

## Interpretation — why the lever doesn't transfer

Reification raises *novelty* because a new atom is a genuinely new primitive: it **enlarges** the space
of constructible organizations, and the novelty metric counts exactly that enlargement. Reification
cannot raise *competence* because competence is measured on the **cross-production network** a
collective forms — closure, breed-true heredity, network breadth — and promoting a competent module to
an **opaque atom moves its internal structure *out* of that measured network**. The atom becomes a
single black-box part with no internal edges; the closure it used to embody is no longer visible as
closure. So reification trades measured competence *inside* the module for a bigger alphabet *outside*
it — a lateral move, not a ratchet. There is no dynamical coupling in which a collective's achieved
competence feeds back to raise the *ceiling* on how competent the next collective can get; the ceiling
is set by the substrate's fixed reaction law, which reification does not touch.

This closes the arc's sharpened open problem with an honest **negative**: the Ω-0.20 rate-not-stock
lever that keeps **novelty** open **does not transfer to competence**. Open-ended novelty and
open-ended competence are genuinely different properties, and the competence plateau is **intrinsic to
selection over a fixed substrate**, not a missing reification step. Compounding competence — a
collective whose competence *keeps rising* — is not achieved by any move the program has: not goal
representation (exp044), not credit assignment (exp045/046), not selection grain (exp047), not
replicating parts (exp048), and not competence reification (exp049).

## Honest scope

Within-substrate measure on the typed_path both-corner base; 6 seeds × 12k ticks × 8 windows. It does
**not** prove no mechanism can compound competence — it shows that the specific, well-motivated lever
(apply Ω-0.20 reification to the closure core) does not, and rules out the last obvious candidate the
arc pointed to. A 2-seed/3k pilot showed closure-reify and freq-reify *byte-identical*; at 6 seeds/12k
they diverge slightly (0.684 vs 0.686, 51 vs 53 atoms) but land on the **same null** — the closure
keying is live but immaterial to the outcome.

## Consequence — the arc's open problem is resolved (negatively)

The real unsolved problem exp048 isolated — *what makes competence a rate, not a stock* — has its first
direct test, and the answer is that **reification is not that coupling**. The competence ceiling is a
property of the substrate's fixed law; changing *what you build on* (a bigger alphabet) does not change
*how good* a collective over that substrate can get. Any future route to compounding competence must
change the **substrate law itself** during the run (make the reaction physics competence-dependent),
not merely grow its alphabet — a qualitatively different and harder move than anything in the arc.

## Reproduce
`PYTHONPATH=. python3 studies/exp049_ceiling.py 12000 6 4000` → the table above; committed as
`studies/exp049_results.json` / `_console.txt`. Pinned by
`test_exp049_competence_reification_promotes_closure_central_modules` (closure-centrality tally lives
and feeds reification; `reify_period=0` ⇒ constructed alphabet frozen). Deterministic across
`PYTHONHASHSEED`; `reify_by`/`reify_period` default ⇒ exp001–048 byte-identical.
