
class Auction:
    def __init__(self, group):
        self.group = group
        self.bids = []
        self.winners = {}

    def validate_bid(
        self,
        ticket_id,
        discount,
        month_no,
        eligible_tickets=None,
        arrears_tickets=None
    ):
        """Validate an auction bid."""

        try:
            discount = float(discount)
            month_no = int(month_no)
        except (ValueError, TypeError):
            return False, "INVALID_AMOUNT_OR_MONTH"

        if discount <= 0:
            return False, "INVALID_DISCOUNT"

        minimum_discount = (
            self.group.chit_value
            * self.group.foreman_commission_pct
            / 100
        )

        if discount < minimum_discount:
            return False, "BELOW_MINIMUM_DISCOUNT"

        if discount % 500 != 0:
            return False, "INVALID_BID_STEP"

        maximum_discount = self.group.chit_value * 0.40

        if discount > maximum_discount:
            return False, "ABOVE_MAXIMUM_DISCOUNT"

        if ticket_id not in self.group.tickets:
            return False, "UNKNOWN_TICKET"

        member = self.group.tickets[ticket_id]

        if member.role == "FOREMAN":
            return False, "FOREMAN_NOT_ELIGIBLE"

        if member.has_won:
            return False, "ALREADY_WON"

        if member.is_defaulter:
            return False, "DEFAULTER_NOT_ELIGIBLE"

        if ticket_id in self.winners.values():
            return False, "ALREADY_WON"

        if eligible_tickets is not None:
            if ticket_id not in eligible_tickets:
                return False, "NOT_ELIGIBLE"

        if arrears_tickets is not None:
            if ticket_id in arrears_tickets:
                return False, "IN_ARREARS"

        return True, "VALID"

    def add_bid(
        self,
        ticket_id,
        month_no,
        discount,
        timestamp=None,
        eligible_tickets=None,
        arrears_tickets=None
    ):
        """Add a valid bid."""

        valid, reason = self.validate_bid(
            ticket_id,
            discount,
            month_no,
            eligible_tickets,
            arrears_tickets
        )

        if not valid:
            return False, reason

        bid = {
            "ticket_id": ticket_id,
            "month_no": int(month_no),
            "discount": float(discount),
            "timestamp": timestamp
        }

        self.bids.append(bid)

        return True, "BID_ACCEPTED"

    def select_winner(self, month_no):
        """Select winner using lowest capped discount."""

        month_bids = [
            bid for bid in self.bids
            if bid["month_no"] == int(month_no)
        ]

        if not month_bids:
            return None

        maximum_discount = self.group.chit_value * 0.40

        for bid in month_bids:
            bid["capped_discount"] = min(
                bid["discount"],
                maximum_discount
            )

        lowest_discount = min(
            bid["capped_discount"]
            for bid in month_bids
        )

        candidates = [
            bid for bid in month_bids
            if bid["capped_discount"] == lowest_discount
        ]

        if len(candidates) == 1:
            winner = candidates[0]
        else:
            winner = self._select_by_lot(
                candidates,
                month_no
            )

        ticket_id = winner["ticket_id"]

        member = self.group.tickets[ticket_id]
        member.has_won = True

        self.winners[int(month_no)] = ticket_id

        result = {
            "group_id": self.group.group_id,
            "month_no": int(month_no),
            "winner_ticket_id": ticket_id,
            "winner_member_id": member.member_id,
            "discount": winner["capped_discount"],
            "prize": (
                self.group.chit_value
                - winner["capped_discount"]
            )
        }

        self.group.auction_records.append(result)

        return result

    def _select_by_lot(self, candidates, month_no):
        """Apply the official deterministic lot rule."""

        candidate_ids = sorted(
            bid["ticket_id"]
            for bid in candidates
        )

        selected_index = (
            self.group.lot_seed * int(month_no)
        ) % len(candidate_ids)

        selected_ticket = candidate_ids[selected_index]

        for bid in candidates:
            if bid["ticket_id"] == selected_ticket:
                return bid

        return candidates[0]

    def run_auction(self, month_no):
        """Run an auction for a particular month."""

        return self.select_winner(month_no)

    def get_winner(self, month_no):
        return self.winners.get(int(month_no))

    def get_bids(self, month_no=None):
        if month_no is None:
            return self.bids.copy()

        return [
            bid for bid in self.bids
            if bid["month_no"] == int(month_no)
        ]
