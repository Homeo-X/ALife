"""
PROJECT Omega -- coupled substrate.

Fix over the original: the kernel-modifier field K now actually affects the
dynamics (it shifts the local growth optimum mu), and K is *inherited* -- when a
pattern grows into new cells, those cells adopt the K of the tissue that spawned
them, plus a small mutation. This is the minimum machinery required for
heritable variation, which is the precondition for selection.

We then test, empirically and against a null control, whether selection actually
operates on K.

Model (Lenia-style):
    M       = convolve(A, ring_kernel)                 # local density
    mu_loc  = mu0 + k_gain * K                          # K sets preferred density (the "gene")
    G       = 2*exp(-((M-mu_loc)^2)/(2 sigma^2)) - 1    # growth in [-1, 1]
    A      <- clip(A + dt*G, 0, 1)

Heredity of K:
    Kbar    = convolve(A*K)/convolve(A)                 # avg gene of nearby living tissue
    birth   = max(dt*G, 0)                              # cells gaining activation
    K      <- K + inherit*birth*(Kbar - K) + mut*(A>eps)   # offspring inherit + mutate
"""
from __future__ import annotations
import numpy as np
from scipy.ndimage import convolve, gaussian_filter


def ring_kernel(radius: float, width: float) -> np.ndarray:
    size = int(2 * radius + 4 * width) + 1
    if size % 2 == 0:
        size += 1
    c = size // 2
    y, x = np.ogrid[-c:c + 1, -c:c + 1]
    d = np.sqrt(x * x + y * y)
    k = np.exp(-((d - radius) ** 2) / (2 * width ** 2))
    k /= k.sum()
    return k


class Substrate:
    def __init__(self, shape=(128, 128), radius=10.0, width=2.0,
                 mu0=0.15, sigma=0.017, dt=0.1,
                 k_gain=0.06, k_max=1.0,
                 inherit=1.0, mutation=0.0, blur=3.0,
                 seed=0):
        self.shape = shape
        self.mu0, self.sigma, self.dt = mu0, sigma, dt
        self.k_gain, self.k_max = k_gain, k_max
        self.inherit, self.mutation, self.blur = inherit, mutation, blur
        self.kernel = ring_kernel(radius, width)
        self.rng = np.random.default_rng(seed)
        self.A = (self.rng.random(shape) < 0.35).astype(float) * self.rng.random(shape)
        # K starts as a smooth random field spanning the whole gene range [-1, 1]
        raw = self.rng.random(shape)
        self.K = (gaussian_filter(raw, sigma=6.0) - 0.5)
        self.K = np.clip(self.K / (np.abs(self.K).max() + 1e-9), -k_max, k_max)

    def step(self) -> None:
        A, K = self.A, self.K
        M = convolve(A, self.kernel, mode='wrap')
        mu_loc = self.mu0 + self.k_gain * K
        G = 2.0 * np.exp(-((M - mu_loc) ** 2) / (2 * self.sigma ** 2)) - 1.0
        self.A = np.clip(A + self.dt * G, 0.0, 1.0)

        # --- inheritance of K along living tissue ---
        eps = 1e-6
        num = convolve(A * K, self.kernel, mode='wrap')
        den = convolve(A, self.kernel, mode='wrap') + eps
        Kbar = num / den
        birth = np.clip(self.dt * G, 0.0, None)          # cells being colonised
        K = K + self.inherit * birth * (Kbar - K)
        if self.mutation > 0:
            K = K + self.mutation * (self.A > 0.05) * self.rng.normal(0, 1, self.shape)
        self.K = np.clip(K, -self.k_max, self.k_max)

    # --- diagnostics: distribution of the gene K weighted by living mass ---
    def mass(self) -> float:
        return float(self.A.sum())

    def gene_stats(self):
        w = self.A
        tot = w.sum()
        if tot < 1e-6:
            return dict(mass=0.0, mean=float('nan'), std=float('nan'))
        mean = float((w * self.K).sum() / tot)
        var = float((w * (self.K - mean) ** 2).sum() / tot)
        return dict(mass=float(tot), mean=mean, std=float(np.sqrt(var)))
