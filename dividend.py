
class Dividend:
    def __init__(self, chit_value, members, commission_pct=5):
        self.chit_value = float(chit_value)
        self.members = int(members)
        self.commission_pct = float(commission_pct)

        if self.chit_value <= 0:
            raise ValueError("Chit value must be positive.")

        if self.members <= 0:
            raise ValueError("Members must be positive.")

        if not 0 <= self.commission_pct <= 100:
            raise ValueError("Invalid commission percentage.")

    def calculate_commission(self):
        return round(
            self.chit_value * self.commission_pct / 100,
            2
        )

    def calculate_dividend(self, discount):
        """
        Calculate distributable dividend.

        Dividend pool = winning discount - foreman commission.
        Per-member dividend is rounded down to whole rupees.
        """
        discount = float(discount)

        if discount < 0:
            raise ValueError("Discount cannot be negative.")

        commission = self.calculate_commission()
        distributable = max(0.0, discount - commission)

        dividend_per_member = int(
            distributable // self.members
        )

        total_dividend = (
            dividend_per_member * self.members
        )

        foreman_remainder = round(
            distributable - total_dividend,
            2
        )

        return {
            "commission": commission,
            "distributable": round(distributable, 2),
            "dividend_per_member": dividend_per_member,
            "foreman_remainder": foreman_remainder
        }

    def calculate_next_subscription(self, dividend_per_member):
        dividend = float(dividend_per_member)

        return max(
            0.0,
            round(self.chit_value / self.members - dividend, 2)
        )


if __name__ == "__main__":
    # Example based on the official GRP-003 month-12 scenario.
    dividend = Dividend(
        chit_value=200000,
        members=40,
        commission_pct=5
    )

    result = dividend.calculate_dividend(15500)

    print("Commission:", result["commission"])
    print("Distributable:", result["distributable"])
    print("Dividend per member:", result["dividend_per_member"])
    print("Foreman remainder:", result["foreman_remainder"])
