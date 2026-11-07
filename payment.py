
from datetime import datetime, date
import math


class Payment:
    def __init__(self, subscription):
        self.subscription = float(subscription)
        self.records = []
        self.penalties = {}

    def calculate_due(self, previous_dividend=0):
        """Calculate net subscription after previous dividend."""
        dividend = float(previous_dividend)

        if dividend < 0:
            raise ValueError("Dividend cannot be negative.")

        return max(0.0, self.subscription - dividend)

    def calculate_late_days(self, payment_date, due_date):
        """Calculate days late after the 10th of the month."""
        paid = self._parse_date(payment_date)
        due = self._parse_date(due_date)

        return max(0, (paid - due).days)

    def calculate_penalty(
        self,
        unpaid_amount,
        days_late,
        annual_monthly_rate=0.01
    ):
        """
        Calculate daily penalty on unpaid amount.

        The supplied sample scenario specifies 1% per month,
        calculated daily for the days late.
        """
        unpaid = float(unpaid_amount)
        days = int(days_late)
        monthly_rate = float(annual_monthly_rate)

        if unpaid < 0 or days < 0 or monthly_rate < 0:
            raise ValueError("Invalid penalty calculation values.")

        return round(
            unpaid * monthly_rate * days / 30,
            2
        )

    def record_payment(
        self,
        ticket_id,
        group_id,
        month_no,
        amount,
        payment_date,
        amount_due=None,
        previous_dividend=0
    ):
        """Record a subscription payment."""

        amount = float(amount)

        if amount <= 0:
            return False, "INVALID_PAYMENT_AMOUNT"

        if amount_due is None:
            amount_due = self.calculate_due(previous_dividend)
        else:
            amount_due = float(amount_due)

        if amount_due < 0:
            return False, "INVALID_AMOUNT_DUE"

        paid_date = self._parse_date(payment_date)

        existing = [
            record for record in self.records
            if record["ticket_id"] == ticket_id
            and record["group_id"] == group_id
            and record["month_no"] == int(month_no)
        ]

        already_paid = sum(
            record["amount_paid"] for record in existing
        )

        remaining_due = max(0.0, amount_due - already_paid)

        accepted_amount = min(amount, remaining_due)
        excess_amount = max(0.0, amount - accepted_amount)

        if accepted_amount > 0:
            record = {
                "ticket_id": ticket_id,
                "group_id": group_id,
                "month_no": int(month_no),
                "amount_due": amount_due,
                "amount_paid": accepted_amount,
                "paid_on": paid_date.isoformat(),
                "days_late": 0,
                "penalty": 0.0,
                "excess_credit": excess_amount
            }

            self.records.append(record)

        else:
            record = {
                "ticket_id": ticket_id,
                "group_id": group_id,
                "month_no": int(month_no),
                "amount_due": amount_due,
                "amount_paid": 0.0,
                "paid_on": paid_date.isoformat(),
                "days_late": 0,
                "penalty": 0.0,
                "excess_credit": amount
            }

            self.records.append(record)

        return True, {
            "accepted_amount": accepted_amount,
            "excess_credit": excess_amount,
            "remaining_due": max(
                0.0,
                amount_due - already_paid - accepted_amount
            )
        }

    def calculate_month_penalty(
        self,
        amount_due,
        amount_paid,
        due_date,
        payment_date
    ):
        """Calculate penalty on the unpaid balance."""

        due = self._parse_date(due_date)
        paid = self._parse_date(payment_date)

        days_late = max(0, (paid - due).days)

        unpaid = max(
            0.0,
            float(amount_due) - float(amount_paid)
        )

        penalty = self.calculate_penalty(
            unpaid,
            days_late
        )

        return {
            "days_late": days_late,
            "unpaid_amount": unpaid,
            "penalty": penalty
        }

    def get_ticket_payments(self, ticket_id):
        return [
            record for record in self.records
            if record["ticket_id"] == ticket_id
        ]

    @staticmethod
    def _parse_date(value):
        if isinstance(value, datetime):
            return value.date()

        if isinstance(value, date):
            return value

        if isinstance(value, str):
            value = value.strip()

            for fmt in (
                "%Y-%m-%d",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M"
            ):
                try:
                    return datetime.strptime(value, fmt).date()
                except ValueError:
                    continue

        raise ValueError(f"Invalid date: {value}")
