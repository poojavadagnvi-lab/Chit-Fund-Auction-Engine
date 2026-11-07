Chit Fund Management System

Project ID: T081-PS-028
Document: Software Design Document
Version: 1.0
Status: Initial Draft
1. Project Overview
The Chit Fund Management System is a command-file-driven software application designed to manage monthly chit fund activities. It automates member payment tracking, late payment penalties, auction processing, prize distribution, dividend calculations, defaulter management, and monthly report generation.

The system will process input files, apply the defined business rules, and generate monthly statements and final account reports. It will operate without a graphical user interface.
2. Project Objectives
   - To maintain member details and payment records.
   - To calculate monthly contributions and late payment penalties.
   - To identify members eligible to participate in auctions.
   - To conduct auctions according to the specified rules.
   - To calculate winners' prize money, foreman commission, and member dividends.
   - To track payment defaults and handle member substitutions.
   - To generate monthly statements and final settlement reports.
3. Scope of the Project
In Scope
- Reading group, member, and command input files.
- Tracking monthly payments and outstanding balances.
- Applying penalties for late payments.
- Checking bidder eligibility.
- Processing auctions and selecting winners.
- Calculating prize amounts, commissions, and dividends.
- Tracking consecutive defaults and guarantor liabilities.
- Generating monthly and final reports.
- Validating input data and handling errors.
Out of Scope
- Online banking and real-time payment gateway integration.
- A graphical user interface or mobile application.
- Automatic transfer of money between bank accounts.
4. Technology Stack
   - Programming Language: Python 3
   - Input Format: CSV files
   - Output Format: Text or CSV reports
   - Version Control: Git and GitHub
   - Testing: Python unit testing
5. System Architecture
The application will follow a modular design.
1. Input Module: Reads group, member, and monthly command files.
2. Validation Module: Checks required fields, data types, and invalid input.
3. Payment Module: Calculates contributions, penalties, and outstanding dues.
4. Eligibility Module: Identifies members who can participate in auctions.
5. Auction Module: Processes bids and selects the winner according to the business rules.
6. Distribution Module: Calculates prize money, foreman commission, and dividends.
7. Default Management Module: Tracks missed payments, defaults, substitutions, and guarantor liabilities.
8. Reporting Module: Generates monthly statements and final settlement reports.
9. Core Data Structures
6.1 Member

The Member object will store information about each chit fund member.

Proposed attributes:
- Member ID
- Member name
- Group ID
- Payment history
- Total amount paid
- Outstanding balance
- Previous auction winner status
- Consecutive default months
- Default status
- Guarantor details, where applicable
- Refund eligibility and settlement details
6.2 Chit Group

The ChitGroup object will represent a chit fund group.

Proposed attributes:
- Group ID
- Total chit value
- Monthly contribution amount
- Total number of months
- Current month
- Random seed for reproducible lottery selection
- List of members
- Auction history
- Monthly dividend records
- Foreman commission records
6.3 Auction Record

The AuctionRecord will store the result of each auction.

Proposed attributes:
- Group ID
- Auction month
- Eligible bidders
- Submitted bids
- Winning member
- Winning discount percentage
- Prize amount
- Foreman commission
- Dividend per member
7. Input and Output File Design
7.1 Input Files

groups.csv

Stores group configuration, including group ID, chit value, duration, and random seed.

members.csv

Stores member details, group membership, and other required member information.

commands.csv

Stores monthly commands or actions that the program must process.

The final column names and command syntax will follow the official project specification.

7.2 Output Files

The application will generate:
- Monthly payment statements.
- Auction result reports.
- Member outstanding balance reports.
- Defaulter and substitution reports.
- Final settlement and account closure reports.
The exact filenames and formats will be finalized during implementation.
8. Business Rules
The application will implement the official business rules identified as BR-01 through BR-15.

The following are the major rule categories based on the currently available project summary:
- BR-01 to BR-03: Monthly contributions, payment deadlines, and late payment penalties.
- BR-04 to BR-06: Bidder eligibility and auction restrictions.
- BR-07 to BR-09: Auction execution, discount limits, and winner selection.
- BR-10 to BR-11: Prize distribution, foreman commission, and dividends.
- BR-12 to BR-13: Default tracking, member replacement, and guarantor liability.
- BR-14 to BR-15: Monthly reporting, refunds, and final account settlement.
Note: This is a provisional grouping, not the verified official mapping. Replace it with the exact BR-01 to BR-15 wording and numbering from the official requirements before submitting the final design document.
9. Processing Workflow
10. Load the group, member, and command files.
11. Validate the input data.
12. Initialize the chit group and member records.
13. Process the current month's payments.
14. Calculate applicable penalties and outstanding balances.
15. Determine eligible bidders.
16. Process the auction or apply the special first-month and final-month rules.
17. Calculate the winner's prize, foreman commission, and member dividends.
18. Update member balances and default records.
19. Generate monthly reports.
20. At the end of the final month, perform the required settlements and close the accounts.
21. Error Handling
The system should handle:
- Missing input files.
- Invalid CSV headers or data types.
- Duplicate member IDs.
- Unknown group or member IDs.
- Invalid payment amounts or bids.
- Missing or malformed monthly commands.
- Invalid auction states.
- Insufficient or inconsistent financial balances.
Errors should produce clear messages. Invalid input must not silently produce incorrect financial results.
11. Testing Strategy
The application will be tested using normal cases, boundary cases, and invalid inputs.

Planned test cases include:
- Payments made before, on, and after the deadline.
- Correct calculation of late payment penalties.
- Members who are eligible and ineligible to bid.
- Minimum and maximum auction discounts.
- Tied bids and auctions with no bids.
- Correct prize, commission, and dividend calculations.
- Consecutive missed payments and member replacement.
- Guarantor liability for a defaulting winner.
- Final refunds and account closure.
- Invalid input files and malformed commands.
Financial calculations will be verified against manually calculated sample cases.
12. Security and Data Integrity
    - Validate all input before processing.
    - Maintain consistent member payment records.
    - Use a fixed random seed where required for reproducible lottery selection.
    - Prevent invalid operations from modifying financial records.
    - Keep clear records of auction outcomes and account changes.
    - Use version control to track code and design changes.
13. Expected Outcome
The expected outcome is a reliable command-line application that automates the major operations of a chit fund group, applies the specified business rules consistently, and produces accurate monthly and final financial reports.
14. Future Enhancements
Possible future improvements include:
- A graphical user interface.
- Database integration.
- Exporting reports to PDF.
- Automated report summaries.
- Secure user authentication.
These enhancements are outside the initial scope unless required by the official project specification.
15. Conclusion
This design document establishes the initial architecture, data structures, processing workflow, and testing approach for the T081-PS-028 Chit Fund Management System. The implementation will follow the official business rules and input/output specifications, with financial calculations validated through testing.