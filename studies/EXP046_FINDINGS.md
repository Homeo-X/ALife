# exp046 — Credit in selection: a heritable per-part contribution model still doesn't compound — the limit is the selection *grain*

exp045 showed that *aiming the goal* at the collective's closure core fails because it moves the goal's
direction but not the selection pressure. exp046 does what that diagnosis demanded — puts credit into
the **fitness** — and finds it still insufficient, isolating the deepest limit yet.

## Mechanism (gated `deme_fitness="credit"`, default off ⇒ exp001–045 byte-identical)

Each deme carries a **heritable per-class contribution map** `_deme_credit: {class → score}`. Every
generation the classes in its autocatalytic **closure core** (producers ∩ products — the parts that
cause self-maintenance) accrue credit (EMA-decayed, `credit_decay=0.9`). Fitness rewards a deme by the
credit still **present** in its current members — so selection directly favours demes that *retain the
parts that make them competent* — and the credit map is inherited at recolonization, so it accumulates
down a lineage: an explicit, evolvable model of *which parts cause competence*. Matched controls: exp038
`closure` (select on instantaneous closure — the snapshot that traded off) and `size` (drift).

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (start → end, mean, slope) | closure (mean) | heredity self |
|-----|:---:|:---:|:---:|
| **credit** (exp046) | 0.66 → 0.68, mean 0.635, **slope −0.008/win** | 0.130 | 0.191 |
| closure-select (exp038) | 0.70 → 0.67, **mean 0.692**, slope +0.005/win | **0.188** | 0.193 |
| size (drift) | 0.64 → 0.55, mean 0.627, slope −0.032/win | 0.097 | 0.268 |

**Verdict: still does not compound — and explicit credit is *worse* than plain closure selection.**

- **Credit-in-selection does not lift competence.** The credit arm's competence (mean 0.635, slope
  −0.008) does **not** rise over generations and is **below** simple instantaneous closure selection
  (0.692), barely clearing the drift floor (0.627).
- **It does not even raise closure — the axis it credits.** Credit closure (0.130) is *below*
  closure-select (0.188). Rewarding demes for *carrying* high-credit classes did not make them more
  self-maintaining than directly selecting closure.

*(Honest process note: a 3-seed / 4k-tick pilot showed a spurious positive — credit rising and beating
both controls. It did not survive 6 seeds / 12k ticks. This is the same lesson the Ω-0.33 determinism
consolidation taught, applied: thin-margin positives from small runs are not trusted until they hold at
scale.)*

## Interpretation — the limit is the selection *grain*, not the credit *signal*

The credit signal is present, heritable, and correct (it does mark the closure-core parts) — yet it
does not help, because **deme-level selection cannot act on it at the right grain.** Selection here
reproduces a *whole deme* by copying a propagule; it can favour a deme that currently *contains*
high-credit parts, but it has no way to preferentially **keep those specific parts** against
within-deme drift, mutation, and recolonization sampling. So the fitness rewards *having* the parts,
not *retaining* them, and the parts wash out just as they did without the credit model — the credit map
becomes a passenger, not a driver. Worse, spending selection on a noisy retention proxy slightly
*underperforms* selecting the outcome (closure) directly.

This is the ROADMAP-predicted outcome: an explicit, heritable contribution signal is **necessary but
not sufficient**, because the missing faculty is not *representing* the credit but *acting* on it at
sub-collective granularity. **The frontier is the selection grain: parts must compete WITHIN the
collective**, not only whole collectives against each other.

The arc, one line each:
- **exp039–042** competence won't compound under fixed / self-expanding scalar objectives → **goal
  representation** missing.
- **exp044** heritable, composable goals → deeper goals accumulate, but transiently, no competence lift.
- **exp045** aim the goal at the closure core → still no compounding → credit is a *representation*
  problem (put it in the fitness).
- **exp046** put an explicit, heritable per-part credit model in the fitness → **still no compounding**,
  because deme-level selection can't retain the credited *parts* → the limit is the **selection grain**
  → within-collective selection.

## Honest scope

Within-substrate measures; one credit rule (closure-core contribution, EMA 0.9, reward present credit).
The negative is robust across 6 seeds and 12k ticks (credit ≤ closure-select on both competence and
closure past the transient). It does **not** prove no credit mechanism can work — it shows *this*
whole-deme-granularity one does not, and diagnoses why (the grain), which is what makes it a signpost:
the next rung must let sub-deme parts be differentially retained.

## Consequence — the named next frontier

exp047: **within-collective selection.** Let the parts of a deme compete *inside* it — e.g. bias which
members survive decay / seed the next generation by their credit (a second, nested selection loop below
the deme), so high-contribution parts are differentially retained within the collective, not just
across collectives. Then test whether competence finally compounds. That is multi-level selection with a
*second* level *below* the deme — the structural move the whole credit-assignment sub-arc points to.

## Reproduce
`PYTHONPATH=. python3 studies/exp046_credit.py 12000 6 4000` → the table above; committed as
`studies/exp046_results.json` / `_console.txt`. Pinned by
`test_exp046_credit_is_heritable_and_rewards_retained_parts` (a heritable, positive credit map is
built; base engine unaffected). Deterministic across `PYTHONHASHSEED`.
