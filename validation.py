
class Validation:

    def validate_member_id(self, member_id, members):
        if not member_id:
            return False, "Member ID is required."

        for member in members:
            if member.get("member_id") == member_id:
                return True, "Valid member ID."

        return False, "Member ID does not exist."

    def validate_group_id(self, group_id, groups):
        if not group_id:
            return False, "Group ID is required."

        for group in groups:
            if group.get("group_id") == group_id:
                return True, "Valid group ID."

        return False, "Group ID does not exist."

    def validate_payment(self, amount):
        try:
            amount = float(amount)

            if amount <= 0:
                return False, "Payment must be greater than zero."

            return True, "Valid payment amount."

        except (ValueError, TypeError):
            return False, "Payment amount must be numeric."

    def validate_bid(self, bid_amount, chit_value):
        try:
            bid_amount = float(bid_amount)
            chit_value = float(chit_value)

            if bid_amount <= 0:
                return False, "Bid must be greater than zero."

            if bid_amount >= chit_value:
                return False, "Bid must be less than chit value."

            return True, "Valid bid amount."

        except (ValueError, TypeError):
            return False, "Invalid bid or chit value."


if __name__ == "__main__":
    validator = Validation()

    print(validator.validate_payment(5000))
    print(validator.validate_payment(-100))
    print(validator.validate_bid(10000, 100000))
