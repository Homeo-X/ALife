# exp066 — Multi-cue perception pays, and only when the cue is relevant (indeed an irrelevant cue *costs*): perceptual breadth is a second route to cognition (Ω-0.55)

exp065 (Ω-0.54) solved a partially-observable world with **memory** — infer the hidden season direction from
history. exp066 asks the complementary question: can an agent solve it instead with a richer **perceptual
channel**, integrating two *observable* cues? The answer is a clean **genome-matched double dissociation**:
integrating a second cue pays *iff* the reward depends on it, and *hurts* when it is present-but-irrelevant.
The result also carries a methodological lesson — the naive control gives a spurious main effect.

## Design (gated; `agent_policy=""` / `env_cues=1` ⇒ exp001–065 byte-identical)

A second **observable** cue — a "regime" `reg = (season_index // feed_bands) % 2` — is **always present and
varying**. Whether the reward depends on it is the environment factor:

- **env_cues=1** — the next band is the sawtooth neighbour `cur+1`; the regime cue **varies but is
  IRRELEVANT** to the reward.
- **env_cues=2** — the next band is a **CONJUNCTION** of season and regime: `cur+1` if `reg=0` else `cur-1`;
  the season alone underdetermines it, so the agent must read **both** cues.

Three arms (2×3), selected by `deme_fitness="anticipation"` (reward products in the next band), anticipation
averaged over ≥ 2 regime periods:

- **embodied** — single-cue *reference*: perceives the season only, a **scalar** phase genome.
- **cue_blind** — the **matched control**: the *identical* per-regime **table** genome as `multi` (same
  parameter count, same mutation load), but its regime percept is **decoupled** (fixed) — it cannot read the
  second cue.
- **multi** — the treatment: perceives the season **and** the regime, acting via the per-regime table.

The decisive contrast is **multi vs cue_blind** — identical genome, the only difference is *reading the
second cue* — so any advantage is **integration**, not extra parameters (the exp062 embodied-vs-blind design
applied to cue 2).

## Result (5 seeds; anticipation over a season cycle; chance = 0.25)

| env_cues | embodied | cue_blind | **multi** | **multi − cue_blind (integration)** | cue_blind − embodied (genome) |
|:---|:---:|:---:|:---:|:---:|:---:|
| 1 (cue varies, irrelevant) | 0.391 | 0.471 | 0.376 | **−0.095** | +0.080 |
| 2 (conjunction — cue relevant) | 0.398 | 0.362 | **0.459** | **+0.097** | −0.036 |

**Integration interaction: +0.193.** Reading the second cue *pays* (+0.097) when the reward depends on it and
*hurts* (−0.095) when it does not — a clean double dissociation against the genome-matched control.

## Interpretation — integration, not parameters; and perception is not free

Two things fall out, and the second is a methodological caution the project's discipline exists to catch:

1. **It is cue INTEGRATION that pays, not a richer policy.** The `cue_blind − embodied` column shows the
   *genome* effect in isolation: simply carrying the per-regime **table** (vs a scalar phase) *raises*
   anticipation by **+0.080** when the cue is irrelevant (env=1) — a lower per-parameter mutation load sits
   tighter to the optimum. A naive `multi vs embodied` contrast therefore shows a **spurious main effect**
   (the table helps in both env's) and would have *wrongly* credited "multi-cue perception" with a benefit
   that is really just parameters. The **matched cue_blind control removes the genome and isolates reading
   the cue** — and that benefit appears *only* under env=2.

2. **Attending to an irrelevant cue actively COSTS.** In env=1 the regime varies but carries no reward
   signal, and `multi` (which conditions its action on it) is **worse** than `cue_blind` (which ignores it):
   fragmenting the policy across a meaningless distinction splits the agent's experience and it learns worse
   (−0.095). Perceptual breadth is not free — integrating an uninformative channel is a liability, the ALife
   analogue of spurious conditioning / over-wide attention. Only when the cue genuinely disambiguates the
   world (env=2) does reading it pay.

Together: **multi-cue perception is a second, distinct route to cognition — perceptual breadth — selectable
exactly when a single cue underdetermines the right action, and penalized when the extra cue is noise.** It
complements exp065's **memory** (depth in time): the triangle POMDP was solvable by *remembering* the hidden
direction (exp065) or by *observing* it as a second cue (exp066). Both are internal capabilities the world's
collectives can be selected to acquire — only when the environment demands them.

## Where this sits in the embodiment thread
- **exp062 (Ω-0.51):** construction agency (perceive→build) **PAYS** — reflex is selectable.
- **exp063 / exp064 (Ω-0.52 / 0.53):** locomotive agency (taxis) does **not** pay — shared-perception
  movement herds.
- **exp065 (Ω-0.54):** **memory** (act on history) pays — only in a partially-observable world.
- **exp066 (Ω-0.55, this):** **multi-cue integration** (act on two observable cues) pays — only when the
  second cue is relevant, and costs when it is not.

## Honest scope
5 seeds; a single second cue with two regimes, a single per-regime table architecture. The direction is
robust and reproduces at single-seed scale (pinned by the test: env=2 multi > cue_blind; interaction > 0.05).
The env=1 *cost* is specific to conditioning behaviour on a varying-but-uninformative cue; a cue that is
constant (not varying) would give no effect rather than a cost. The result does **not** claim this is the
best perceptual architecture — only that the *simplest* two-cue integrator is selected **iff** the second
cue disambiguates the reward, and is penalized otherwise, cleanly separated from the parameter-count
confound. `agent_policy=""` / `env_cues=1` ⇒ exp001–065 byte-identical; deterministic across `PYTHONHASHSEED`.

## Reproduce
`PYTHONPATH=. python3 studies/exp066_multicue.py 5 7000 2400` → the table above; committed as
`studies/exp066_results.json` / `_console.txt`. Pinned by
`test_exp066_multi_cue_perception_pays_only_when_the_cue_is_relevant` (`agent_policy=""` / `env_cues=1`
byte-identical to exp036; multi acts; the genome-matched double dissociation: multi > cue_blind in the
conjunctive env, with the env=2 − env=1 integration gap > 0.05).
