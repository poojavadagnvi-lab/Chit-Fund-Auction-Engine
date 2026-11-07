
import csv
import os


class Member:
    def __init__(
        self,
        member_id,
        name,
        group_id=None,
        ticket_id=None,
        gender=None,
        mobile=None,
        kyc_pan=None,
        role="MEMBER",
        joined_month=1,
        replaces_ticket="NONE"
    ):
        self.member_id = member_id
        self.name = name
        self.group_id = group_id
        self.ticket_id = ticket_id
        self.gender = gender
        self.mobile = mobile
        self.kyc_pan = kyc_pan
        self.role = role
        self.joined_month = int(joined_month)
        self.replaces_ticket = replaces_ticket

        self.total_paid = 0.0
        self.payments = []
        self.is_defaulter = False
        self.has_won = False


class ChitGroup:
    def __init__(
        self,
        group_id,
        chit_value,
        members=None,
        subscription=None,
        foreman_commission_pct=5,
        auction_day=15,
        start_month=None,
        lot_seed=0,
        duration=None,
        random_seed=None
    ):
        self.group_id = group_id
        self.chit_value = float(chit_value)

        self.members_count = int(
            members if members is not None else 0
        )

        self.subscription = float(
            subscription if subscription is not None
            else (
                self.chit_value / self.members_count
                if self.members_count else 0
            )
        )

        self.foreman_commission_pct = float(
            foreman_commission_pct
        )
        self.auction_day = int(auction_day)
        self.start_month = start_month

        self.lot_seed = int(
            lot_seed if random_seed is None else random_seed
        )

        self.duration = int(
            duration if duration is not None
            else self.members_count
        )

        self.random_seed = self.lot_seed
        self.members = []
        self.tickets = {}
        self.current_month = 0
        self.payment_records = []
        self.auction_records = []


class ChitFundEngine:
    def __init__(
        self,
        groups_file="groups.csv",
        members_file="members.csv"
    ):
        self.groups_file = groups_file
        self.members_file = members_file

        self.groups = {}
        self.members = {}
        self.tickets = {}

    def load_groups(self):
        if not os.path.exists(self.groups_file):
            raise FileNotFoundError(
                f"Groups file not found: {self.groups_file}"
            )

        self.groups.clear()

        with open(
            self.groups_file,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                group_id = row["group_id"].strip()

                group = ChitGroup(
                    group_id=group_id,
                    chit_value=row["chit_value"],
                    members=row["members"],
                    subscription=row["subscription"],
                    foreman_commission_pct=(
                        row.get("foreman_commission_pct") or 5
                    ),
                    auction_day=row.get("auction_day") or 15,
                    start_month=row.get("start_month"),
                    lot_seed=row.get("lot_seed") or 0
                )

                self.groups[group_id] = group

        return self.groups

    def load_members(self):
        if not os.path.exists(self.members_file):
            raise FileNotFoundError(
                f"Members file not found: {self.members_file}"
            )

        if not self.groups:
            self.load_groups()

        self.members.clear()
        self.tickets.clear()

        for group in self.groups.values():
            group.members.clear()
            group.tickets.clear()

        with open(
            self.members_file,
            "r",
            newline="",
            encoding="utf-8-sig"
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:
                ticket_id = row["ticket_id"].strip()
                group_id = row["group_id"].strip()
                member_id = row["member_id"].strip()

                if group_id not in self.groups:
                    raise ValueError(
                        f"Unknown group ID: {group_id}"
                    )

                member = Member(
                    member_id=member_id,
                    name=row["name"].strip(),
                    group_id=group_id,
                    ticket_id=ticket_id,
                    gender=row.get("gender"),
                    mobile=row.get("mobile"),
                    kyc_pan=row.get("kyc_pan"),
                    role=row.get("role") or "MEMBER",
                    joined_month=row.get("joined_month") or 1,
                    replaces_ticket=(
                        row.get("replaces_ticket") or "NONE"
                    )
                )

                if ticket_id in self.tickets:
                    raise ValueError(
                        f"Duplicate ticket ID: {ticket_id}"
                    )

                self.tickets[ticket_id] = member
                self.members[ticket_id] = member

                self.groups[group_id].members.append(member)
                self.groups[group_id].tickets[ticket_id] = member

        return self.members

    def create_member(self, member_id, name, group_id=None):
        member = Member(
            member_id=member_id,
            name=name,
            group_id=group_id
        )

        self.members[member_id] = member

        if group_id in self.groups:
            self.groups[group_id].members.append(member)

        return member

    def record_payment(self, member_id, amount):
        amount = float(amount)

        if amount <= 0:
            print("Payment must be greater than zero.")
            return False

        member = self.members.get(member_id)

        if member is None:
            print(f"Member not found: {member_id}")
            return False

        member.total_paid += amount

        payment = {
            "member_id": member_id,
            "ticket_id": member.ticket_id,
            "amount": amount
        }

        member.payments.append(payment)

        for group in self.groups.values():
            if member in group.members:
                group.payment_records.append(payment)
                break

        print(f"\nPayment recorded for {member.name}")
        print(f"Amount paid: Rs. {amount:.2f}")
        print(f"Total paid: Rs. {member.total_paid:.2f}")

        return True

    def get_group(self, group_id):
        return self.groups.get(group_id)

    def get_member(self, member_id):
        return self.members.get(member_id)

    def get_ticket(self, ticket_id):
        return self.tickets.get(ticket_id)

    def display_groups(self):
        for group in self.groups.values():
            print(
                f"{group.group_id}: "
                f"Chit value Rs. {group.chit_value:.2f}, "
                f"Members {group.members_count}, "
                f"Subscription Rs. {group.subscription:.2f}"
            )

    def display_members(self):
        for member in self.members.values():
            print(
                f"{member.ticket_id} - "
                f"{member.name} - "
                f"{member.group_id}"
            )


if __name__ == "__main__":
    engine = ChitFundEngine()

    engine.load_groups()
    engine.load_members()

    print("\nGroups loaded:", len(engine.groups))
    print("Tickets loaded:", len(engine.tickets))

    engine.display_groups()
