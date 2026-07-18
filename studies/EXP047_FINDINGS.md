# exp047 — Within-collective selection *collapses* the collective: competence is irreducibly collective (the arc's terminal diagnosis)

exp046 traced the failure of credit-in-the-fitness to the selection **grain**: deme-level reproduction
copies a whole propagule and cannot retain the credited *parts*. exp047 adds the missing grain — a
second selection level *below* the deme — and finds it does not rescue compounding; it **collapses the
collective**, which turns out to be the deepest and most informative result of the whole
self-improvement arc.

## Mechanism (gated `within_select`, default off ⇒ exp001–046 byte-identical)

Built on exp046 (`deme_fitness="credit"` + the heritable per-class credit map + the exp040 heredity
channel). When founding an offspring, `within_select=True` draws the propagule from the source deme's
members **sampled with probability rising in their credit** (Efraimidis–Spirakis weighted sampling
without replacement, with a floor so zero-credit members keep a chance) — so the parts the deme's
credit map has learned cause its competence are differentially transmitted: parts competing *inside*
the collective, not only whole collectives against each other. (A strict top-k by credit collapses
diversity outright; the probabilistic bias is the fair, gentler form — and it still collapses, below.)
Matched control: exp046 (`within_select=False`).

## Result (12k ticks, 6 seeds, `memory_horizon=4000`)

| arm | competence (mean, slope) | network survival (frac of demes) |
|-----|:---:|:---:|
| **within** (exp047) | **0.363, −0.021/win** | **0.29** |
| credit (exp046) | 0.615, −0.008/win | 0.43 |
| size (drift) | 0.613, −0.032/win | 0.36 |

**Verdict: within-collective selection *collapses* the collective — decisively worse on both axes.**

- **Competence falls, not rises.** The within arm's competence (mean 0.363, declining) is far *below*
  deme-only credit (0.615) and the drift floor (0.613) — the opposite of compounding.
- **The network itself collapses.** Network survival drops to **0.29** of demes (vs 0.43 for credit):
  biasing reproduction toward high-credit members erodes the **diversity** the cross-production network
  requires, so fewer demes sustain a network at all.

## Interpretation — competence is irreducibly collective; the arc's terminal diagnosis

The reason within-collective selection backfires is the deepest point the arc reaches: **the credited
parts have no value in isolation.** A deme's competence (closure, breed-true heredity, breadth) is a
property of a *diverse, complementary cross-production network* — members that produce *each other*. A
part earns "credit" only because of its role in that network; select hard for those parts as
individuals and you strip out the complementary partners, so the network — and the competence it
carried — falls apart. Part-level selection on credit is therefore **self-defeating**: it destroys the
collective context that made the credit meaningful. This is the classic multi-level-selection tension
(strong within-group selection undermines the group), here shown to be *fatal* to collective
competence in this substrate.

That closes the credit-assignment sub-arc with a structural conclusion, not another mechanism to try:
**collective competence is not decomposable into independently selectable part contributions.** Credit
assignment fails not because credit can't be represented (exp046 represented it fine) or acted on at
the right grain (exp047 acted on it), but because the credit is **not localizable to parts** —
it lives in the relations between them.

**The terminal diagnosis connects the arc back to its own origin (exp012).** Compounding
self-improvement of a collective would require its parts to be **replicators** — units that carry and
copy their *own* heritable value independent of context — so that selecting them preserves rather than
destroys value. The type-path parts are not replicators; they are context-dependent network
components. exp012 already found the one place genuine replicators emerged (behaviour-first SKI soup,
`C·x → C`); the self-improvement arc shows that *without* part-level replicators, no amount of goal
representation (exp044), goal alignment (exp045), credit in fitness (exp046), or within-collective
selection (exp047) makes collective competence compound.

The arc, one line each:
- **exp039–042** competence won't compound under fixed / self-expanding scalar objectives → **goal
  representation** missing.
- **exp044** heritable, composable goals → deeper goals accumulate, but transiently, no competence lift.
- **exp045** aim the goal at the closure core → credit is a *representation* problem (put it in fitness).
- **exp046** credit in the fitness → still no compounding → the selection *grain* is wrong.
- **exp047** within-collective selection → **collapses the collective** → competence is **irreducibly
  collective**; compounding needs **part-level replicators** (the exp012 lesson), which this substrate
  lacks.

## Honest scope

Within-substrate measures; one within-selection rule (credit-weighted propagule). The collapse is
robust across 6 seeds and 12k ticks (within < credit on both competence and network survival every
seed-averaged window past the transient), and holds for both the strict-top-k and the gentler
weighted form — the tension is not a tuning artifact: *any* strength of part-selection that is strong
enough to matter erodes the diversity the collective needs. It does not prove no substrate can make
collective competence compound — it shows *this* one cannot via selection alone, and identifies the
missing ingredient (part-level replicators), which is a substrate property, not a selection rule.

## Consequence — the arc rests here

The self-improvement arc (exp036–047) is complete as a falsifiable sequence: it systematically ruled
out every selection/representation route to compounding collective competence and terminated in a
structural reason — **competence is irreducibly collective, and its parts are not replicators.** The
honest next move is not another deme-selection knob but a *substrate* question, and the program already
has the thread: revisit exp012's genuine replicators and ask whether a substrate whose parts are
themselves replicators (carrying heritable, context-independent value) lets collective competence
compound — closing the loop from the arc's end back to its beginning.

## Reproduce
`PYTHONPATH=. python3 studies/exp047_within.py 12000 6 4000` → the table above; committed as
`studies/exp047_results.json` / `_console.txt`. Pinned by
`test_exp047_within_selection_biases_the_propagule_by_credit` (`within_select` gated; off ⇒ exp046
byte-identical; the heritable credit map still builds). Deterministic across `PYTHONHASHSEED`.
