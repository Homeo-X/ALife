"""
PROJECT Omega -- geometry coupling (a landscape that deforms under its occupants).

Previous model: the gene K shifted the growth optimum mu. That is a STATIC
fitness landscape -- there is one best mu, the population climbs to it, done.

Here the gene K instead sets each cell's *interaction radius* by blending a small
and a large ring kernel per cell:

    a       = (K + 1) / 2                       in [0, 1]  (per cell)
    M       = (1 - a) * conv(A, k_small)  +  a * conv(A, k_large)
    G       = 2*exp(-((M - mu)^2)/(2 sigma^2)) - 1
    A      <- clip(A + dt*G, 0, 1)

Why the landscape can now move: the density M a cell perceives depends on how
mass is spatially arranged at *its* radius. That arrangement is produced by the
geometries of the surrounding cells. So the fitness of "radius K" depends on the
K-composition of the neighbourhood -- frequency-dependent selection. Whether that
actually yields a non-stationary landscape (moving optimum / branching / no ESS)
or merely a new fixed point is an empirical question this file lets us answer.

K inheritance is unchanged: offspring adopt neighbour-tissue K plus mutation.
"""
from __future__ import annotations
import numpy as np
from scipy.ndimage import convolve, gaussian_filter
from omega_coupled import ring_kernel


class GeoSubstrate:
    def __init__(self, shape=(96, 96), r_lo=7.0, r_hi=13.0, width=1.8,
                 mu=0.15, sigma=0.02, dt=0.15,
                 k_max=1.0, inherit=1.0, mutation=0.01, blur_r=9.0,
                 mode="geometry", k_gain=0.10, seed=0):
        self.shape = shape
        self.mu, self.sigma, self.dt = mu, sigma, dt
        self.k_max, self.inherit, self.mutation = k_max, inherit, mutation
        self.mode = mode                       # "geometry" or "mu" (static-landscape control)
        self.k_gain = k_gain
        self.k_small = ring_kernel(r_lo, width)
        self.k_large = ring_kernel(r_hi, width)
        self.k_mid = ring_kernel(0.5 * (r_lo + r_hi), width)   # used for K inheritance transport
        self.blur_r = blur_r
        self.rng = np.random.default_rng(seed)
        self.A = (self.rng.random(shape) < 0.35).astype(float) * self.rng.random(shape)
        raw = self.rng.random(shape)
        self.K = gaussian_filter(raw, sigma=6.0) - 0.5
        self.K = np.clip(self.K / (np.abs(self.K).max() + 1e-9), -k_max, k_max)
        self.G = np.zeros(shape)

    def _density(self):
        if self.mode == "geometry":
            a = (self.K + 1.0) * 0.5
            Ms = convolve(self.A, self.k_small, mode="wrap")
            Ml = convolve(self.A, self.k_large, mode="wrap")
            M = (1.0 - a) * Ms + a * Ml
            mu = self.mu
        else:  # "mu" : static-landscape control (single radius, K shifts optimum)
            M = convolve(self.A, self.k_mid, mode="wrap")
            mu = self.mu + self.k_gain * self.K
        return M, mu

    def step(self):
        A, K = self.A, self.K
        M, mu = self._density()
        G = 2.0 * np.exp(-((M - mu) ** 2) / (2 * self.sigma ** 2)) - 1.0
        self.G = G
        self.A = np.clip(A + self.dt * G, 0.0, 1.0)
        # inheritance of K along living tissue
        eps = 1e-6
        num = convolve(A * K, self.k_mid, mode="wrap")
        den = convolve(A, self.k_mid, mode="wrap") + eps
        Kbar = num / den
        birth = np.clip(self.dt * G, 0.0, None)
        K = K + self.inherit * birth * (Kbar - K)
        if self.mutation > 0:
            K = K + self.mutation * (self.A > 0.05) * self.rng.normal(0, 1, self.shape)
        self.K = np.clip(K, -self.k_max, self.k_max)

    # ---- diagnostics ----
    def mass(self):
        return float(self.A.sum())

    def gene_stats(self):
        w = self.A
        tot = w.sum()
        if tot < 1e-6:
            return dict(mass=0.0, mean=float("nan"), std=float("nan"))
        mean = float((w * self.K).sum() / tot)
        var = float((w * (self.K - mean) ** 2).sum() / tot)
        return dict(mass=float(tot), mean=mean, std=float(np.sqrt(var)))

    def realized_landscape(self, nbins=16):
        """A-weighted mean growth G per K-bin among currently living cells.
        This is the fitness landscape as actually experienced *right now*. If the
        landscape is static its peak stays put; if it deforms the peak moves."""
        edges = np.linspace(-1, 1, nbins + 1)
        centers = 0.5 * (edges[:-1] + edges[1:])
        F = np.full(nbins, np.nan)
        occ = np.zeros(nbins)
        idx = np.clip(np.digitize(self.K, edges) - 1, 0, nbins - 1)
        live = self.A > 0.05
        for b in range(nbins):
            sel = live & (idx == b)
            w = self.A[sel]
            if w.sum() > 1e-6:
                F[b] = float((w * self.G[sel]).sum() / w.sum())
                occ[b] = float(w.sum())
        return centers, F, occ

    def occupancy_hist(self, nbins=16):
        edges = np.linspace(-1, 1, nbins + 1)
        centers = 0.5 * (edges[:-1] + edges[1:])
        idx = np.clip(np.digitize(self.K, edges) - 1, 0, nbins - 1)
        h = np.zeros(nbins)
        live = self.A > 0.05
        for b in range(nbins):
            h[b] = self.A[live & (idx == b)].sum()
        s = h.sum()
        return centers, (h / s if s > 0 else h)
