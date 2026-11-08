# Access Review Automator

A Python script that automates a recurring (90-day) user access review.
It reads a list of accounts and flags the ones that need action:

- **Terminated users who are still enabled**
- **Accounts inactive for 90+ days**
- **Admin rights held outside the approved admin group** (least privilege)

## Why I built it
In my security work, I run recurring 90-day access reviews to keep access least-privilege.
This project automates the manual parts of that process so reviews are faster and consistent.

## How to run
1. Install Python 3.
2. In this folder, run: `python access_review.py`
3. Results print to the screen and save to `access_review_report.csv`.

## Sample output
```
Reviewed 7 accounts; 4 findings.
- tchen (Marketing): Admin rights outside approved group - right-size access
- rpatel (Finance): Terminated user still enabled - disable now
- agarcia (HR): Inactive 157 days - remove or disable
- dwilson (Operations): Inactive 128 days - remove or disable
Report saved to access_review_report.csv
```
(Day counts change depending on when you run it.)

## Data
`sample_users.csv` contains **fake sample data only**.

## Ideas to extend
- Read users directly from Active Directory or Microsoft Entra ID (via Microsoft Graph)
- Email the report to account owners
- Add a configurable list of approved admins
