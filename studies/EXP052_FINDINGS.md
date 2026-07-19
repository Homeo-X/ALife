# exp052 — The Red Queen: a coevolutionary target raises the competence *ceiling* to the arc's highest, but competence still does **not** compound

The self-improvement arc (exp044–049) established that collective competence never compounds — it
plateaus at a substrate-set ceiling under every selection/representation/replicator/reification route.
The common thread: selection is against a **fixed target**, and exp042's self-expanding scalar bar
failed because a single global number chasing the frontier flattens its own gradient. exp052 grounds a
**receding** target in real, local rivals — the biological driver of open-ended competence (an arms
race) — the boldest untried lever, run under strong controls.

## Mechanism (gated `deme_fitness="redqueen"`, default off ⇒ exp001–051 byte-identical)

A deme is rewarded for **(a) its own autocatalytic closure** and **(b) the fraction of its closure core
(producers ∩ products) a spatial rival cannot yet produce** — a zero-sum, *closure-aligned* antagonism.
As the rival co-acquires those classes, the deme's advantage vanishes and it must innovate **new closed
structure**, so the gradient does not vanish (the flaw a relative-competence bar and exp042's scalar
share), and — because the reward is *within the self-maintaining core* — out-racing the rival **builds
competence** rather than idiosyncratic dead-ends. *(This is the principled form: raw offense/defense
promoted dead-end novelty and collapsed diversity; a relative-competence bar inherited exp042's
vanishing gradient; the closure-aligned zero-sum rule is what survived.)*

**The decisive control** is `coevolve_frozen`: identical fitness form, but rival producers are a **frozen
snapshot** captured at `freeze_gen` (a fixed target, no arms race) — isolating the *receding* target from
the fitness form.

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (mean, slope) | closure (mean) | live-deme survival | classes |
|-----|:---:|:---:|:---:|:---:|
| **coevolve** (live rival — receding target) | **0.820**, −0.021/win | **0.255** | **0.56 → 0.73** | 5,505 |
| frozen (rival frozen at freeze_gen) | 0.630, −0.011/win | 0.187 | 0.55 | 4,441 |
| closure (exp038 static-competence selection) | 0.673, +0.004/win | 0.191 | 0.57 | 4,594 |
| drift (size) | 0.615, −0.031/win | 0.096 | 0.35 | 3,308 |

**Verdict: the wall holds — competence is still a *stock*, not a *rate* — but the receding target is the
arc's strongest ceiling-lifter.**

- **The receding target does large, real work.** coevolve competence (**0.820**) is the **highest of any
  arm**, beating the frozen control by **+0.190**, plain closure selection by **+0.147**, and drift by
  +0.205. The **coevolve − frozen** gap isolates the effect to the target *receding* (identical fitness
  form): a live, co-adapting rival lifts competence far above a fixed one. coevolve also has the highest
  closure (0.255), the most construction (5,505 classes), and — unlike exp047's within-collective
  selection — the **healthiest, rising network survival** (0.56 → 0.73): no collapse.
- **But competence does not compound.** coevolve's slope is **−0.021/win** — high-and-flat-to-declining,
  not rising. The arms race sets a higher *plateau* but does not tilt the *trajectory* upward. This is
  the **same "level, not rate" pattern as exp048** (part-level replicators lifted the ceiling ~2× without
  changing the slope) — here in its strongest form, and now on the *same* substrate as its controls.

## Interpretation — the highest ceiling yet, still a ceiling

exp052 is the first mechanism in the whole arc to raise competence **above plain closure selection on the
same substrate** — exp045/046 *under*-performed closure, exp047 *collapsed* it, and exp048 needed a
different (combinator) substrate to lift it. A grounded, receding coevolutionary target is therefore the
best competence-*level* lever the program has found, and the closure-aligned design keeps networks
healthy (survival rises) where naive antagonism collapsed them. Yet it lands on the arc's now-familiar
wall: **competence is a stock, not a rate.** Even a receding target — the mechanism biology uses to drive
open-ended arms races — raises *how competent* collectives get without making competence *keep rising*.
Why: with a fixed substrate law, the arms race quickly reaches a mutual-escape equilibrium (everyone
running to stay in place — coevolve survival and competence are high and steady, the relative advantage
flat), and there is no dynamical coupling that turns achieved competence into a *higher achievable*
competence. The receding target moves the plateau; it does not remove the ceiling.

This sharpens, rather than overturns, the arc's conclusion. **Open-ended novelty ≠ open-ended
competence** (Ω-0.39/0.40 vs Ω-0.38) still holds: construction compounds, competence plateaus — now shown
against the strongest lever, which raises the plateau most but still cannot make competence a rate. The
one class of move still untried remains the substrate-law change exp049 named (a **Catalytic Law** —
promote competent closure loops to shared *reactions*, not opaque atoms). The user's staged plan —
combine the Red Queen with the Catalytic Law (exp053) — is the natural next rung: the Red Queen supplies
the highest plateau and the receding pressure; the Catalytic Law would supply the substrate-level
feedback that could turn that pressure into a rising ceiling.

## Honest scope

Within the both-corner typed_path substrate; 6 seeds × 12k ticks × 8 windows. The coevolve slope is
mildly negative (−0.021), driven partly by a final-window dip; the safe reading is **flat-to-declining,
not rising** — no compounding. The **level** effect (coevolve ≫ frozen/closure/drift) is large and robust
across the run. The mechanism was iterated to its principled form before measuring (three variants); the
committed version is the closure-aligned zero-sum rule.

## Reproduce
`PYTHONPATH=. python3 studies/exp052_redqueen.py 12000 6 4000` → the table above; committed as
`studies/exp052_results.json` / `_console.txt`. Pinned by
`test_exp052_redqueen_scores_against_a_coevolving_or_frozen_rival` (a network + competence are built; the
live arm freezes no rival while the frozen control captures a full-coverage snapshot). Deterministic
across `PYTHONHASHSEED`; `deme_fitness` default ⇒ exp001–051 byte-identical.
