"""A fixed-memory *global* novelty estimator — the instrument that settles "stays open forever".

The novelty rate (new classes/tick) is the anti-closure signal. On short runs it is exact: the
universe's ``classes_ever_seen`` counter increments once per class that registers while absent from
``class_registry`` (``universe.observe_classes``). But a *long* run must bound memory
(``memory_horizon``), which evicts cold class records — so an evicted class that *reappears*
re-registers and is **counted again**. The measured novelty rate then becomes horizon-windowed and
inflated, and a positive long-run rate cannot be distinguished from the same classes recycling
through the eviction window (exp032's "positive-floor vs slow-dilution" open edge).

``GlobalNoveltySketch`` removes that inflation with fixed memory: an approximate "ever seen" set of
class identities that survives eviction. It is a **scalable Bloom filter** — a growing list of
bit-slices — so the aggregate false-positive rate stays bounded no matter how many distinct classes
ever appear (a single fixed filter would fill up and its rising false-positive rate would manufacture
a *spurious* novelty decay, confounding the exact question). Two invariants make it scientifically
safe:

  * **Repeats are never counted as new** (no Bloom false negatives): anything already inserted always
    tests present, so an evicted class that reappears is *always* recognized as old. This strips
    **all** eviction-recycling inflation — the whole point of the instrument.
  * **Genuine novelty is only ever *under*-counted**, by at most the aggregate false-positive rate
    (~1%): a brand-new class that happens to collide with already-set bits is missed. So the estimate
    is **conservative** — it can only ever *lower* the measured novelty, never inflate it, and thus
    cannot fabricate open-endedness. The scalable design holds that ~1% bias flat across the whole run
    (a single fixed filter would fill and its rising FPR would manufacture a spurious novelty decay).

Stdlib only: hashing is ``hashlib.blake2b`` with a per-hash personalization, so the sketch is fully
deterministic and seed-free (no dependence on Python's randomized ``hash``).
"""
from __future__ import annotations

import hashlib
import math


class _BloomSlice:
    """One fixed-capacity Bloom filter over a bit array (``bytearray``)."""

    __slots__ = ("m", "k", "_bits", "count", "capacity")

    def __init__(self, capacity: int, fp_rate: float) -> None:
        capacity = max(1, capacity)
        # optimal bits m and hashes k for a target false-positive rate p:
        #   m = -n ln p / (ln 2)^2 ,  k = (m/n) ln 2
        m = int(math.ceil(-capacity * math.log(fp_rate) / (math.log(2) ** 2)))
        m = max(8, m)
        self.m = m
        self.k = max(1, int(round((m / capacity) * math.log(2))))
        self._bits = bytearray((m + 7) // 8)
        self.count = 0            # distinct elements added to THIS slice
        self.capacity = capacity  # design capacity before FPR degrades

    def _positions(self, key: bytes):
        # Kirsch–Mitzenmacher double hashing from one blake2b digest → k bit positions.
        h = hashlib.blake2b(key, digest_size=16).digest()
        h1 = int.from_bytes(h[:8], "big")
        h2 = int.from_bytes(h[8:], "big") | 1   # odd, so the stride never degenerates
        for i in range(self.k):
            yield (h1 + i * h2) % self.m

    def __contains__(self, key: bytes) -> bool:
        b = self._bits
        for pos in self._positions(key):
            if not (b[pos >> 3] >> (pos & 7)) & 1:
                return False
        return True

    def add(self, key: bytes) -> None:
        b = self._bits
        for pos in self._positions(key):
            b[pos >> 3] |= 1 << (pos & 7)
        self.count += 1

    def is_full(self) -> bool:
        return self.count >= self.capacity


class GlobalNoveltySketch:
    """Scalable approximate 'ever-seen' set of class identities, with fixed-ish memory.

    A new bit-slice is appended (with larger capacity and a tightened false-positive target, so the
    geometric series of per-slice rates sums to a bounded aggregate) whenever the current head fills.
    Membership tests all slices; insertion goes to the head. Total memory grows only ~logarithmically
    in the number of distinct classes, and the aggregate false-positive rate stays below the target.
    """

    __slots__ = ("_slices", "_growth", "_ratio", "_fp0", "distinct")

    def __init__(self, initial_capacity: int = 1 << 16, fp_rate: float = 0.005,
                 growth: int = 4, tightening: float = 0.5) -> None:
        # aggregate FPR <= fp0 * (1 / (1 - tightening)); with fp0=0.005, tightening=0.5 => <= 0.01
        self._fp0 = fp_rate
        self._growth = growth
        self._ratio = tightening
        self._slices = [_BloomSlice(initial_capacity, fp_rate)]
        self.distinct = 0           # count of elements reported NEW (deduplicated ever-seen count)

    def _key(self, cls: str) -> bytes:
        return cls.encode("utf-8", "surrogatepass")

    def __contains__(self, cls: str) -> bool:
        key = self._key(cls)
        return any(key in s for s in self._slices)

    def add_if_new(self, cls: str) -> bool:
        """Return True the first time ``cls`` is seen (and record it); False if already seen.

        Never a false negative (a truly-new id is always reported new); a false positive only causes
        an under-count (a new id mistaken for seen), never an over-count.
        """
        key = self._key(cls)
        for s in self._slices:
            if key in s:
                return False
        head = self._slices[-1]
        if head.is_full():
            cap = head.capacity * self._growth
            fp = self._fp0 * (self._ratio ** len(self._slices))
            head = _BloomSlice(cap, fp)
            self._slices.append(head)
        head.add(key)
        self.distinct += 1
        return True

    def memory_bytes(self) -> int:
        return sum(len(s._bits) for s in self._slices)
