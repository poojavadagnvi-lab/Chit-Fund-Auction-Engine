# PS-028 – Chit Fund Auction Engine with Dividend Distribution and Defaulter Handling — Sample Data Pack

Prepared by 10 SECONDS for Team T081.

## Files

| File | What it holds | Row count |
|---|---|---|
| `groups.csv` | Chit groups (3) with value, size, subscription, commission, auction day, start month and lot seed | 3 |
| `members.csv` | One row per ticket (original tickets joined_month 1; substitutes later) with KYC | 88 |
| `commands.txt` | Every month of every group: subscriptions, bids, auctions, sureties, substitutions, termination, print commands | 3065 |

Row count for `commands.txt` = command lines (comment lines starting with `#` and blank lines are not counted).

## Column reference

### groups.csv
| column | type | format | notes |
|---|---|---|---|
| group_id | string | `GRP-001` … | |
| chit_value | money | Rs | = subscription × members |
| members | int | | number of tickets = number of months |
| subscription | money | Rs | gross monthly subscription per ticket |
| foreman_commission_pct | number | `5` | 5% of chit value per month |
| auction_day | int | day of month | AUCTION command timestamp is 11:00:00 on this day |
| start_month | string | `YYYY-MM` | month 1 of the group |
| lot_seed | int | | lot rule: sort the candidate ticket_ids ascending and pick index `(lot_seed × month_no) mod count` |

### members.csv (one row per ticket)
| column | type | format | notes |
|---|---|---|---|
| ticket_id | string | `TKT-0001` … | primary key; a member with two tickets has two rows |
| group_id | string | FK → groups | |
| member_id | string | `MBR-001` / `FRM-001` | FRM = foreman's own ticket (receives the month-1 prize without auction) |
| name, gender | string | | gender `M`/`F` |
| mobile | string | 10 digits | |
| kyc_pan | string | PAN-shaped | fake |
| role | string | `FOREMAN` / `MEMBER` | |
| joined_month | int | | 1 = original roll; substitutes join later |
| replaces_ticket | string | ticket_id or `NONE` | substitute tickets name the removed ticket |

### commands.txt
Money as Rs with 2 decimals; month_no is 1-based within the group; timestamps `YYYY-MM-DD HH:MM:SS`.

## Command file format

One command per line, `COMMAND|arg1|...`, strictly in file order (the file is chronological across all three groups). `#` lines are comments.

| command | arguments | meaning |
|---|---|---|
| `SUBSCRIPTION` | `ticket_id`, `group_id`, `month_no`, `timestamp`, `amount` | payment of that month's net subscription; due by the 10th |
| `BID` | `group_id`, `month_no`, `ticket_id`, `timestamp`, `discount` | bid = discount forgone (Rs). Always precedes the month's AUCTION |
| `AUCTION` | `group_id`, `month_no`, `timestamp` | conduct the auction for the month using the BIDs received since the previous AUCTION |
| `SURETY` | `ticket_id`, `group_id`, `month_no`, `date`, `surety1_name`, `surety1_income`, `surety2_name`, `surety2_income` | sureties furnished by the month's winner (declared monthly income) |
| `BANK_GUARANTEE` | `ticket_id`, `group_id`, `month_no`, `date`, `bank`, `ref`, `amount` | alternative to sureties |
| `SUBSTITUTE` | `group_id`, `month_no`, `old_ticket_id`, `new_ticket_id`, `timestamp`, `amount_paid` | new member takes over a removed ticket, paying all past net subscriptions (months 1..month_no) at once |
| `TERMINATE` | `group_id`, `timestamp` | last month: no auction; last unpaid ticket receives chit value − commission; produce the termination account |
| `PRINT_STATEMENT` | `group_id`, `month_no` | emit the monthly chit statement |
| `PRINT_TERMINATION` | `group_id` | emit the termination account |

Conventions (stated here because the brief is silent): remaining months for the surety threshold = members − month_no; dividend of month N is divided by the group size (the roll is always full at auction time); the lot rule is in groups.csv notes; bids are capped at 40% before comparison.

## Planted scenarios

Locators below are physical line numbers of the named file (a CSV header is line 1; comment lines in commands.txt count).

Edge cases from the brief (one bullet per edge case, in brief order):

- **Bid exactly at 40% and one at 40% + Rs 500** — GRP-001 month 6 (chit 100000.00, max discount 40000.00): BID by TKT-0006 for 40000.00 (line 1661) and BID by TKT-0007 for 40500.00 (line 1659) → the second is capped to 40000.00, both tie at the cap → winner by lot: sort tied ticket_ids ascending and take index (lot_seed × month_no) mod count (lot_seed 4121 from groups.csv). AUCTION at line 1662.
- **Dividend division leaving a remainder** — GRP-003 month 12 (40 members, commission 10000.00): winning discount 15500.00 → distributable 5500.00 / 40 = 137.50 → dividend 137 per member (rounded down), remainder Rs 20 retained by the foreman (AUCTION line 546). Note: with Rs 500 bid steps and 5% commission the remainder can only be 0 or 20 in the 40-member group and is always 0 in the 20- and 25-member groups, so this is the only remainder configuration the data can contain.
- **Member paying on the 10th at 23:59 vs 11th** — GRP-001 month 3: TKT-0004 pays at 2025-05-10 23:59:00 (line 1351, on time, no penalty) and TKT-0005 pays at 2025-05-11 00:30:00 (line 1352, 1 day late → penalty 1% per month computed daily from the 11th on the unpaid amount for 1 day; still paid before the 15th auction so eligible to bid).
- **Member with 2 tickets winning on one and defaulting on the other** — GRP-002: member MBR-029 holds TKT-0029 and TKT-0030 (members.csv). TKT-0029 wins the month-5 auction (AUCTION line 1056); TKT-0030 stops paying from month 8 (no SUBSCRIPTION lines for it from month 8) → DEFAULTER after months 8–9, removed at the month-12 review, substituted in month 13 (SUBSTITUTE line 1838). The winning ticket keeps receiving dividends and must keep paying; the defaulting ticket is treated per the defaulter rules.
- **No eligible bidders in a month** — GRP-001 month 3: no BID lines precede the AUCTION at line 1357 → prize by lot among eligible members at the minimum discount (5000.00 = commission → dividend 0). Lot rule as in edge case 1.
- **Substitution in the final month** — GRP-001: TKT-0009 misses months 15–19 → DEFAULTER at the month-16 review, removed at the month-19 review; SUBSTITUTE in month 20 (the final month, no auction) at line 3050 — the new ticket pays all 20 past net subscriptions at once and, being the only ticket that has not won, receives chit value minus commission at termination (TERMINATE line 3064).
- **Surety income exactly at the threshold** — GRP-002 month 7 winner TKT-0033: remaining months after the auction = 18 → threshold = 2 × 10000 × 18 / 12 = 30000.00; SURETY line 1253 declares both incomes as exactly 30000.00 → valid, prize paid within 7 days. Contrast: month-9 winner TKT-0034 furnishes one surety at 20000.00 (line 1458, below threshold 26666.67 → prize held) and later a BANK_GUARANTEE (line 1466) that releases it.
- **Defaulter removed then group terminated before 3 months** — GRP-003: TKT-0054 misses months 33–37 → DEFAULTER at the month-34 review, removed at the month-37 review, SUBSTITUTE in month 38 (line 2851); the group terminates in month 40 (TERMINATE line 3067), less than 3 months after the removal → the removed member's refund (subscriptions paid − penalties − 5% of chit value) is settled only in the termination account.

Extra traps:

- GRP-003 TKT-0058 wins month 10 (AUCTION line 455) and stops paying from month 30 → a defaulter who has already won: not removed, pursued through sureties for the remaining subscriptions; it still receives dividends.
- GRP-003 TKT-0049 misses months 38–40 → DEFAULTER at the month-39 review but the group ends at month 40 before any removal; handle in the termination account.
- Invalid bids that must be rejected: GRP-001 month 8 bid by a ticket that already won (line 1856); GRP-002 month 10 bid by TKT-0030 while in arrears (line 1551); GRP-003 month 15 bids of 12300.00 (not a Rs 500 step, line 684) and 9500.00 (below the 5% minimum of 10000.00, line 682).
- Duplicate subscription: TKT-0035 month 6 is paid twice with the same timestamp (lines 1085 and 1086) → second payment is an excess credit, not a second month's subscription.
- SUBSCRIPTION amounts are the net subscription due for that month (subscription − previous month's dividend per member). Penalties are never included in a SUBSCRIPTION line; they accrue on the ledger and are settled in the termination account.

## What is NOT in this pack

Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-nn). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.


## Output format expected at evaluation

1. `monthly_statements.csv` — one row per group per month: `group_id, month_no, month (YYYY-MM), winner_ticket_id, winner_member_id, discount, prize, foreman_commission, dividend_per_member, foreman_remainder, next_month_subscription, eligible_bidders, defaulters (semicolon list of ticket_ids), penalties_accrued_this_month, prize_status (PAID/HELD)`.
2. `member_ledger.csv` — one row per ticket per month: `group_id, ticket_id, month_no, amount_due, amount_paid, paid_on, days_late, penalty, dividend_received, status (ACTIVE/DEFAULTER/REMOVED/SUBSTITUTE/WON)`.
3. `termination_account.csv` — one row per group: `group_id, total_subscriptions_collected, total_prizes_paid, total_commission, penalties_collected, removed_member_refunds, sureties_pursued_amount, foreman_net`.
4. `rejections.csv` — `line_no, command, group_id, ticket_id, reason_code` for every rejected BID / SUBSCRIPTION / SURETY.
