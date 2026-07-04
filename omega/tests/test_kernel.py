"""Unit tests for the immutable kernel: identity, distinguishability, causality."""
from __future__ import annotations

import unittest

from omega.kernel.organization import Organization, canonical_cls, distinguishability
from omega.kernel.transform import Reaction
from omega.kernel.universe import Universe


class TestOrganization(unittest.TestCase):
    def test_distinguishability_counts_atoms(self):
        self.assertEqual(distinguishability(("A",)), 1)
        self.assertEqual(distinguishability(("bond", "A", "B")), 3)
        self.assertEqual(distinguishability((("A", "B"), ("C",))), 3)
        self.assertEqual(distinguishability(()), 0)

    def test_identity_is_recognizability(self):
        # same state -> same class, regardless of uid/history
        a = Organization(uid=1, state=("A", "B"))
        b = Organization(uid=999, state=("A", "B"), birth_tick=50, lineage=(3, 4))
        self.assertEqual(a.cls, b.cls)
        # different arrangement -> different class
        c = Organization(uid=2, state=("B", "A"))
        self.assertNotEqual(a.cls, c.cls)

    def test_canonical_hash_is_stable(self):
        self.assertEqual(canonical_cls(("x", ("y", "z"))), canonical_cls(("x", ("y", "z"))))

    def test_depth(self):
        self.assertEqual(Organization(0, ("A",)).depth, 1)
        self.assertEqual(Organization(0, ("A", ("B", "C"))).depth, 2)


class TestUniverseCausality(unittest.TestCase):
    def test_spawn_and_dissolve_conserve(self):
        u = Universe(total_quanta=100)
        org = u.spawn(("A", "B", "C"), kind="x")  # binds 3
        self.assertIsNotNone(org)
        self.assertEqual(u.reservoir, 97)
        u.verify()
        u.dissolve(org.uid)
        self.assertEqual(u.reservoir, 100)
        u.verify()

    def test_spawn_blocked_when_reservoir_insufficient(self):
        u = Universe(total_quanta=2)
        self.assertIsNone(u.spawn(("A", "B", "C"), kind="x"))  # needs 3, has 2
        self.assertEqual(u.reservoir, 2)

    def test_reaction_conserves_and_records_births(self):
        u = Universe(total_quanta=100)
        a = u.spawn(("A",), kind="m")
        b = u.spawn(("B",), kind="m")
        r = Reaction(inputs=(a.uid, b.uid), consume=(a.uid, b.uid),
                     outputs=((("bond", "A", "B"), "c"),), via="bind")
        self.assertTrue(u.apply_reaction(r))
        u.verify()
        # two monomers (2 quanta) -> one composite (3 quanta); net 1 drawn from reservoir
        self.assertEqual(u.reservoir, 100 - 3)
        self.assertEqual(u.class_births[canonical_cls(("bond", "A", "B"))], 1)

    def test_reaction_blocked_leaves_world_untouched(self):
        u = Universe(total_quanta=2)  # only 2 free
        a = u.spawn(("A",), kind="m")  # binds 1, reservoir now 1
        before = dict(u.organizations)
        # output needs 3 quanta, only 1 free + 1 freed = 2 available -> blocked
        r = Reaction(inputs=(a.uid,), consume=(a.uid,),
                     outputs=((("x", "y", "z"), "c"),), via="grow")
        self.assertFalse(u.apply_reaction(r))
        self.assertEqual(u.organizations, before)
        u.verify()


if __name__ == "__main__":
    unittest.main()
