"""
Does selection actually act on the gene K?

Treatment : k_gain > 0  -> K shifts the local growth optimum (K affects survival)
Control   : k_gain = 0  -> K is inherited & tracked identically but is inert

Both start from IDENTICAL A and K fields (same seed). If selection is real, the
living-mass-weighted distribution of K in the treatment must diverge from the
control: its mean moves toward the fittest K and/or its variance is culled below
the neutral baseline. The control subtracts out the neutral smoothing that
inheritance alone produces.
"""
import numpy as np
from omega_coupled import Substrate

SHAPE = (96, 96)
STEPS = 500
SEEDS = [1, 2, 3, 4, 5]
COMMON = dict(shape=SHAPE, radius=9, width=1.8, mu0=0.15, sigma=0.02,
              dt=0.15, k_max=1.0, inherit=1.0, mutation=0.01)
K_GAIN = 0.10


def run(seed, k_gain):
    s = Substrate(seed=seed, k_gain=k_gain, **COMMON)
    rows = []
    for t in range(STEPS):
        s.step()
        if t % 50 == 49:
            g = s.gene_stats()
            rows.append((t + 1, g["mass"], g["mean"], g["std"]))
    return rows


def main():
    print(f"grid={SHAPE} steps={STEPS} k_gain(treat)={K_GAIN} "
          f"mutation={COMMON['mutation']} seeds={SEEDS}\n")
    # collect final-window stats across seeds
    agg = {"treat": {"mean": [], "std": []}, "ctrl": {"mean": [], "std": []}}
    for seed in SEEDS:
        tr = run(seed, K_GAIN)
        ct = run(seed, 0.0)
        # print seed 1 full trajectory as an illustration
        if seed == SEEDS[0]:
            print("  seed 1 trajectory (t | mass | K_mean | K_std)")
            print("  TREATMENT                         CONTROL")
            for a, b in zip(tr, ct):
                print(f"   t={a[0]:3d} m={a[1]:7.0f} mean={a[2]:+.3f} std={a[3]:.3f}"
                      f"   |   m={b[1]:7.0f} mean={b[2]:+.3f} std={b[3]:.3f}")
            print()
        # final-window (last reading) aggregate
        agg["treat"]["mean"].append(tr[-1][2]); agg["treat"]["std"].append(tr[-1][3])
        agg["ctrl"]["mean"].append(ct[-1][2]);  agg["ctrl"]["std"].append(ct[-1][3])

    def ms(x): return f"{np.mean(x):+.3f} ± {np.std(x):.3f}"
    print(f"Final K_mean  treatment: {ms(agg['treat']['mean'])}   "
          f"control: {ms(agg['ctrl']['mean'])}")
    print(f"Final K_std   treatment: {np.mean(agg['treat']['std']):.3f} ± {np.std(agg['treat']['std']):.3f}   "
          f"control: {np.mean(agg['ctrl']['std']):.3f} ± {np.std(agg['ctrl']['std']):.3f}")
    # paired variance-reduction test
    dstd = np.array(agg["ctrl"]["std"]) - np.array(agg["treat"]["std"])
    print(f"\nPer-seed variance culling (ctrl_std - treat_std): "
          f"{np.round(dstd,3).tolist()}")
    print(f"mean={dstd.mean():+.3f}  (positive = treatment narrows the gene "
          f"pool more than neutral drift => selection)")


if __name__ == "__main__":
    main()
