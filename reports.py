
import csv


class Reports:

    def generate_member_report(
        self, members, filename="member_report.csv"
    ):
        if not members:
            print("No member data available.")
            return

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=members[0].keys()
            )

            writer.writeheader()
            writer.writerows(members)

        print("Member report generated successfully:", filename)

    def generate_payment_report(
        self, payments, filename="payment_report.csv"
    ):
        if not payments:
            print("No payment data available.")
            return

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=payments[0].keys()
            )

            writer.writeheader()
            writer.writerows(payments)

        print("Payment report generated successfully:", filename)

    def generate_auction_report(
        self, auctions, filename="auction_report.csv"
    ):
        if not auctions:
            print("No auction data available.")
            return

        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=auctions[0].keys()
            )

            writer.writeheader()
            writer.writerows(auctions)

        print("Auction report generated successfully:", filename)


if __name__ == "__main__":

    report = Reports()

    sample_members = [
        {
            "member_id": "M001",
            "member_name": "Rahul",
            "group_id": "G001"
        },
        {
            "member_id": "M002",
            "member_name": "Priya",
            "group_id": "G001"
        }
    ]

    sample_payments = [
        {
            "member_id": "M001",
            "group_id": "G001",
            "amount": 5000,
            "month": "January"
        }
    ]

    report.generate_member_report(sample_members)
    report.generate_payment_report(sample_payments)
