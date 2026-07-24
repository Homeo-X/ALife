# exp062 — Embodied agency is SELECTABLE: a perception→action policy is selected and pays dose-dependently — the world's collectives are agents (Ω-0.51)

The living world sustains open-ended novelty and self-maintaining life at scale (Ω-0.48–0.50). exp062 opens
the **embodiment / minds** thread with its first falsifiable rung: are the world's collectives *agents* — do
they perceive their environment and act on it, and is that selected? It answers **yes**.

## Mechanism — a heritable perception→action policy, vs a perception-ablated control (gated, off ⇒ byte-identical)

An **agent** is a collective with a heritable policy. It **perceives** the environment's season (the cyclic
feed band, exp036 — which atoms the world favours now) and **acts** by foraging atoms from the band an
offset `phi` from the *perceived* season; foraged atoms become material the deme builds with. Selection is
`deme_fitness="anticipation"` (reward products matching the *next* band), so an agent that evolves `phi=1`
forages the next band and anticipates. `phi` is a heritable genome (`_deme_phase`, mirroring exp037's
`_deme_res`) — inherited at propagule founding, mutated. The decisive matched control **`agent_policy=
"blind"`** has the *identical* policy + forage repertoire but a **fixed percept** (decoupled from the real,
moving season): same action, no sensing. This isolates whether *perception that informs action* is what pays.
Swept as a **dose-response in the action strength** (`forage_n`). `agent_policy=""` (default) ⇒ exp001–061
byte-identical.

## Result (6 seeds; anticipation averaged over a full season cycle; φ=1 = the anticipatory phase, chance = 1/4)

| forage_n (action strength) | embodied anticip | blind anticip | **advantage** | embodied φ=1 | blind φ=1 |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 2 (weak) | 0.275 | 0.256 | **+0.020** | **0.47** | 0.18 |
| 6 | 0.393 | 0.294 | **+0.099** | 0.66 | 0.10 |
| 12 (strong) | 0.694 | 0.523 | **+0.171** | 0.76 | 0.06 |

**Verdict: agency is selectable — perception is *used and selected*, and it *pays*, dose-dependently.**

- **Perception is selected (φ concentrates at the informative phase).** Embodied agents' policies concentrate
  at **φ=1** — the phase that acts on the *perceived* next season — well above chance (0.47 → 0.76 as the
  signal strengthens). Blind agents, whose percept is decoupled, concentrate *away* from φ=1 (0.18 → 0.06):
  no phase helps them, so their policies drift/fix elsewhere. The world **selects for using information about
  the environment** — the defining property of a mind, in miniature.
- **Perception pays, dose-dependently.** At weak action the embodied advantage over blind is negligible
  (+0.020 — the policy is selected but the behaviour barely moves the deme). As the action gains teeth the
  advantage **grows monotonically to +0.171** (embodied 0.694 vs blind 0.523, both far above chance 0.25):
  a stronger perception-coupled action produces a proportionally larger fitness advantage. Sensing-and-acting
  is not just representable and selected — it is **behaviourally advantageous**, and more so the more the
  agent can act.
- **The blind control is the right one.** Blind agents *do* forage and *do* rise above chance at strong
  action (0.523) — foraging any band helps a little when it happens to align — but they **cannot track** the
  moving season with a fixed percept, so they plateau ~0.17 below the embodied agents that read the live
  environment. The gap is the value of *perception itself*, cleanly isolated.

## Interpretation — the world is not just alive; its collectives are agents

This is the first evidence that the built world supports **agency**, the substrate-native minimal mind: a
collective that perceives its environment, acts on that perception with a heritable policy, and is *selected*
for doing so, with the behavioural payoff scaling with how much it can act. It sits naturally atop the arc —
the same heritable-per-collective-genome machinery that carried construction rules (exp037), goals (exp044),
credit (exp046), and policy phase here — now closing a **perceive → act → select** loop. The world Ω-0.48–50
showed to be open-ended and self-maintaining is also, at least in miniature, **inhabited by agents**.

## Honest scope
6 seeds. This is a *proto*-mind, deliberately minimal: the percept is one scalar (the season), the policy is
one heritable integer (`phi`), the action is foraging. It establishes that perception-coupled action is
selectable and dose-dependently advantageous — **not** that the agents have rich internal models, planning,
or multi-cue perception (those are later rungs). The anticipation metric is a cycle average (robust to the
season phase, unlike a single-tick snapshot, which flatters the fixed-percept blind agent). `agent_policy=""`
⇒ exp001–061 byte-identical; deterministic across `PYTHONHASHSEED`.

## Reproduce
`PYTHONPATH=. python3 studies/exp062_agency.py 6 6000 1200` → the table above; committed as
`studies/exp062_results.json` / `_console.txt`. Pinned by
`test_exp062_embodied_agency_is_selected_and_is_byte_identical_off` (`agent_policy=""` ⇒ exp036 byte-identical;
embodied concentrates φ at the anticipatory phase and out-anticipates blind). Next rungs: richer perception
(multi-cue), a policy with internal state / memory, and action on *space* (perceive neighbours → migrate).
