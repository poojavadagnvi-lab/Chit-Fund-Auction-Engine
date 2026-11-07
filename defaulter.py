
class DefaulterManager:
    def __init__(self, group, defaulter_after=2, removal_after=5):
        self.group = group
        self.defaulter_after = defaulter_after
        self.removal_after = removal_after

        self.payment_history = {}
        self.defaulter_tickets = set()
        self.removed_tickets = set()

    def get_ticket(self, ticket_id):
        """Find a ticket in the group."""
        tickets = getattr(self.group, "tickets", {})

        if ticket_id in tickets:
            return tickets[ticket_id]

        members = getattr(self.group, "members", [])

        for member in members:
            if getattr(member, "ticket_id", None) == ticket_id:
                return member

        return None

    def record_payment_status(self, ticket_id, month_no, paid):
        """Record whether a ticket paid its subscription for a month."""

        if self.get_ticket(ticket_id) is None:
            raise ValueError("Ticket not found: " + ticket_id)

        if month_no <= 0:
            raise ValueError("Month number must be positive.")

        if not isinstance(paid, bool):
            raise ValueError("Payment status must be True or False.")

        if ticket_id not in self.payment_history:
            self.payment_history[ticket_id] = {}

        self.payment_history[ticket_id][month_no] = paid

    def count_consecutive_missed_months(self, ticket_id, month_no):
        """Count consecutive unpaid months ending at the given month."""

        history = self.payment_history.get(ticket_id, {})
        missed_months = 0

        current_month = month_no

        while current_month >= 1:
            if history.get(current_month, False):
                break

            missed_months += 1
            current_month -= 1

        return missed_months

    def review_month(self, month_no):
        """Review payments and update defaulter/removal status."""

        if month_no <= 0:
            raise ValueError("Month number must be positive.")

        results = []

        tickets = getattr(self.group, "tickets", {})

        for ticket_id, member in tickets.items():

            role = str(getattr(member, "role", "")).lower()

            # Foreman tickets are not treated as defaulters.
            if role == "foreman":
                continue

            # Skip tickets already removed.
            if ticket_id in self.removed_tickets:
                continue

            missed_months = self.count_consecutive_missed_months(
                ticket_id, month_no
            )

            if missed_months >= self.defaulter_after:

                member.is_defaulter = True
                self.defaulter_tickets.add(ticket_id)

                status = "DEFAULTER"

                # A winning ticket cannot be removed.
                if getattr(member, "has_won", False):
                    status = "DEFAULTER - WINNING TICKET PROTECTED"

                elif missed_months >= self.removal_after:
                    self.removed_tickets.add(ticket_id)
                    member.is_removed = True
                    status = "REMOVED"

                results.append({
                    "ticket_id": ticket_id,
                    "month_no": month_no,
                    "missed_months": missed_months,
                    "status": status
                })

            else:
                results.append({
                    "ticket_id": ticket_id,
                    "month_no": month_no,
                    "missed_months": missed_months,
                    "status": "ACTIVE"
                })

        return results

    def is_defaulter(self, ticket_id):
        return ticket_id in self.defaulter_tickets

    def is_removed(self, ticket_id):
        return ticket_id in self.removed_tickets

    def get_defaulters(self):
        return sorted(self.defaulter_tickets)

    def get_removed_tickets(self):
        return sorted(self.removed_tickets)


if __name__ == "__main__":
    print("Defaulter Manager module loaded successfully.")
