
import unittest
from types import SimpleNamespace

from defaulter import DefaulterManager


class TestDefaulterManager(unittest.TestCase):

    def setUp(self):
        member = SimpleNamespace(
            ticket_id="TKT-0001",
            role="member",
            has_won=False,
            is_defaulter=False
        )

        self.group = SimpleNamespace(
            tickets={"TKT-0001": member},
            members=[]
        )

        self.manager = DefaulterManager(
            self.group,
            defaulter_after=2,
            removal_after=5
        )

    def test_two_consecutive_missed_payments(self):
        self.manager.record_payment_status("TKT-0001", 1, False)
        self.manager.record_payment_status("TKT-0001", 2, False)

        results = self.manager.review_month(2)

        self.assertTrue(self.manager.is_defaulter("TKT-0001"))
        self.assertEqual(results[0]["status"], "DEFAULTER")

    def test_five_consecutive_missed_payments(self):
        for month in range(1, 6):
            self.manager.record_payment_status(
                "TKT-0001", month, False
            )

        results = self.manager.review_month(5)

        self.assertTrue(self.manager.is_removed("TKT-0001"))
        self.assertEqual(results[0]["status"], "REMOVED")

    def test_winning_ticket_is_not_removed(self):
        self.group.tickets["TKT-0001"].has_won = True

        for month in range(1, 6):
            self.manager.record_payment_status(
                "TKT-0001", month, False
            )

        results = self.manager.review_month(5)

        self.assertTrue(self.manager.is_defaulter("TKT-0001"))
        self.assertFalse(self.manager.is_removed("TKT-0001"))
        self.assertEqual(
            results[0]["status"],
            "DEFAULTER - WINNING TICKET PROTECTED"
        )

    def test_paid_month_resets_missed_count(self):
        self.manager.record_payment_status("TKT-0001", 1, False)
        self.manager.record_payment_status("TKT-0001", 2, False)
        self.manager.record_payment_status("TKT-0001", 3, True)

        count = self.manager.count_consecutive_missed_months(
            "TKT-0001", 3
        )

        self.assertEqual(count, 0)


if __name__ == "__main__":
    unittest.main()
