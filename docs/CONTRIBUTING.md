# Contributing

Project Ω is a **falsifiable lab notebook**, not a typical app. The contribution unit is not a
feature — it is a **claim tested against a control**. A few conventions keep the science honest and
the engine trustworthy; please follow them.

## The shape of a contribution

1. **One yes/no question.** Frame the work as a single falsifiable question with a *matched control*
   and a *predicted falsification condition* ("if X, then the hypothesis is wrong"). Negative and
   retracted results are first-class here (see exp009/010/011/028/036 and the retracted exp003).
2. **A gated mechanism.** New physics goes into `omega/experiments/exp012_combinator.py` (or a new
   module) as a **new knob that defaults to inert**, so every prior experiment stays *byte-identical*
   when it is off. No RNG may be consumed on the default path.
3. **A matched-control study.** Add `studies/expNNN_*.py` that prints a **rate metric** (never a
   cumulative count — the program has two metric-artefact false positives on record) comparing
   treatment vs control, and a short `studies/EXPNNN_FINDINGS.md` stating the honest verdict.
4. **A pinned claim test.** Add `test_expNNN_*` to `omega/tests/test_experiments.py` capturing the
   result as a regression guard.
5. **A milestone note.** Summarize in `omega/docs/RESEARCH_LOG.md` in the log's voice.

## Non-negotiables

- **Determinism.** A run is a pure function of its seed. `python -m unittest
  omega.tests.test_experiments.TestDeterminism` must stay green, and a fixed-seed
  `(final_population, final_classes_total)` must be unchanged when your knob is off.
- **Byte-identity.** Verify exp001–latest are byte-identical with your feature disabled (diff a
  fixed-seed run before/after your change).
- **No third-party dependencies.** Pure Python 3.10+ standard library. The substrate must be
  auditable end-to-end; anything importing the engine must run with a bare interpreter.
- **Honesty over polish.** State results as the evidence supports them, including "no" and "not
  yet". Rates in temporal windows; matched controls; report which corner fails and when.

## Running things

```bash
python -m unittest discover -s omega/tests -t .   # the whole suite (also runs in CI)
python -m omega.cli list                          # experiments
PYTHONPATH=. python3 studies/exp030_*.py          # a study
python -m omega.world run --dashboard             # the living world
```

## Style

Match the surrounding code: comment density, naming, and the "why" comments that tie each knob to
the experiment it serves. Keep changes small and reviewable; one experiment per pull request.
