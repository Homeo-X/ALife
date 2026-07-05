"""
Does the fitness landscape deform under its own occupants?

Rigorous test: pairwise invasibility (PIP). For each resident gene r we grow a
homogeneous resident population to equilibrium, implant a small patch of mutant
gene m, and ask whether the mutant mass grows (invades).

Reading a PIP:
  * A STATIC landscape has an ESS: some resident r* that NO mutant can invade
    (its row is all "-"). Evolution climbs to r* and stops. Convergent.
  * A landscape that DEFORMS under its occupants has NO ESS: every resident is
    invadable by something, and/or invasion is frequency dependent (whether m
    beats r depends on r). Non-convergent / open-ended-ish.

We run this for two couplings:
  mode="mu"        : gene shifts growth optimum  -> expected STATIC (ESS present)
  mode="geometry"  : gene sets interaction radius -> the thing under test
The mu-model doubles as a positive control that the PIP method finds an ESS when
one exists.
"""
import numpy as np
from omega_geo import GeoSubstrate

GRID = (64, 64)
VALUES = np.array([-0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6])
EQUIL = 300          # steps to grow resident to equilibrium
INVADE = 150         # steps to test mutant growth
PATCH = 18           # side of central mutant patch


def mutant_mass(sub, r, m):
    """Living mass on the mutant side of the r/m midpoint."""
    mid = 0.5 * (r + m)
    live = sub.A > 0.05
    if m >= r:
        sel = live & (sub.K > mid)
    else:
        sel = live & (sub.K < mid)
    return float(sub.A[sel].sum())


def equilibrate(mode, r, seed=0):
    sub = GeoSubstrate(shape=GRID, mode=mode, mutation=0.0, seed=seed)
    sub.K[:] = r
    for _ in range(EQUIL):
        sub.step()
        sub.K[:] = r          # pin resident gene while it settles
    return sub.A.copy()


def invades(mode, r, m, A_eq, seed=0):
    sub = GeoSubstrate(shape=GRID, mode=mode, mutation=0.0, seed=seed)
    sub.A = A_eq.copy()
    sub.K[:] = r
    h, w = GRID
    y0, x0 = h // 2 - PATCH // 2, w // 2 - PATCH // 2
    sub.K[y0:y0 + PATCH, x0:x0 + PATCH] = m
    m0 = mutant_mass(sub, r, m)
    for _ in range(INVADE):
        sub.step()
    m1 = mutant_mass(sub, r, m)
    if m0 < 1e-3:
        return np.nan, m0, m1
    return (m1 - m0) / (m0 + 1.0), m0, m1     # normalised mutant growth


def pip(mode):
    print(f"\n===== PIP  mode={mode}  (rows=resident r, cols=mutant m) =====")
    A_eqs = {}
    resid_mass = {}
    for r in VALUES:
        A = equilibrate(mode, r)
        A_eqs[r] = A
        resid_mass[r] = float(A.sum())
    header = "  r\\m  " + "".join(f"{m:+.1f} " for m in VALUES) + "  resid_mass"
    print(header)
    S = np.zeros((len(VALUES), len(VALUES)))
    for i, r in enumerate(VALUES):
        cells = ""
        for j, m in enumerate(VALUES):
            if abs(m - r) < 1e-9:
                cells += "  .  "
                S[i, j] = 0
                continue
            score, m0, m1 = invades(mode, r, m, A_eqs[r])
            if np.isnan(score):
                cells += "  ?  "
                S[i, j] = np.nan
            else:
                S[i, j] = score
                cells += " +  " if score > 0.05 else (" -  " if score < -0.05 else " 0  ")
        print(f" {r:+.1f}  {cells}   {resid_mass[r]:7.0f}")
    # ESS check: a resident whose row is all non-positive (no mutant invades)
    ess = []
    for i, r in enumerate(VALUES):
        row = S[i]
        others = [row[j] for j in range(len(VALUES)) if j != i and not np.isnan(row[j])]
        if others and all(v <= 0.05 for v in others):
            ess.append(r)
    print(f"  -> ESS candidates (row all non-positive => uninvadable): "
          f"{[f'{v:+.1f}' for v in ess] if ess else 'NONE'}")
    return S, ess


def free_run(mode, steps=1000, seed=3):
    sub = GeoSubstrate(shape=(96, 96), mode=mode, mutation=0.01, seed=seed)
    means = []
    for t in range(steps):
        sub.step()
        if t % 25 == 24:
            means.append(sub.gene_stats()["mean"])
    # is the mean still moving late, or flatlined?
    late = np.array(means[-8:])
    drift_late = float(np.abs(np.diff(late)).mean())
    _, hist = sub.occupancy_hist(nbins=16)
    # crude modality count: local maxima above 0.6*peak
    peak = hist.max()
    modes = 0
    for b in range(1, len(hist) - 1):
        if hist[b] > 0.6 * peak and hist[b] >= hist[b - 1] and hist[b] >= hist[b + 1]:
            modes += 1
    print(f"\n free-run mode={mode}: final K_mean={means[-1]:+.3f}  "
          f"late-drift/25steps={drift_late:.4f}  occupancy_modes~{modes}")
    return means


def main():
    print("FREE EVOLUTION (does the gene keep moving or flatline?)")
    free_run("mu")
    free_run("geometry")
    pip("mu")
    pip("geometry")


if __name__ == "__main__":
    main()
