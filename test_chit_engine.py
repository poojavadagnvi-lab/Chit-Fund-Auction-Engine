
import unittest

from chit_engine import ChitFundEngine, Member


class TestChitFundSystem(unittest.TestCase):

    def setUp(self):
        self.engine = ChitFundEngine()

    def test_member_creation(self):
        member = Member("M001", "Member1")

        self.assertEqual(member.member_id, "M001")
        self.assertEqual(member.name, "Member1")
        self.assertFalse(member.has_won)

    def test_invalid_payment(self):
        member = Member("M001", "Member1")
        self.engine.members["M001"] = member

        result = self.engine.record_payment("M001", -500)

        self.assertFalse(result)
        self.assertEqual(member.total_paid, 0)

    def test_payment_recorded(self):
        member = Member("M001", "Member1")
        self.engine.members["M001"] = member

        result = self.engine.record_payment("M001", 5000)

        self.assertTrue(result)
        self.assertEqual(member.total_paid, 5000)

    def test_load_groups(self):
        self.engine.load_groups()

        self.assertEqual(len(self.engine.groups), 3)
        self.assertIn("GRP-001", self.engine.groups)
        self.assertIn("GRP-002", self.engine.groups)
        self.assertIn("GRP-003", self.engine.groups)

        group = self.engine.groups["GRP-001"]

        self.assertEqual(group.chit_value, 100000)
        self.assertEqual(group.members_count, 20)

    def test_load_members(self):
        self.engine.load_groups()
        self.engine.load_members()

        self.assertEqual(len(self.engine.tickets), 88)
        self.assertEqual(len(self.engine.members), 88)

        self.assertIn("TKT-0001", self.engine.tickets)

        member = self.engine.tickets["TKT-0001"]

        self.assertEqual(member.group_id, "GRP-001")
        self.assertEqual(member.role, "FOREMAN")

    def test_group_ticket_counts(self):
        self.engine.load_groups()
        self.engine.load_members()

        total_tickets = sum(
            len(group.members)
            for group in self.engine.groups.values()
        )

        self.assertEqual(total_tickets, 88)


if __name__ == "__main__":
    unittest.main()
