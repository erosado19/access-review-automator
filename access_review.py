"""
Access Review Automator
Flags user accounts that should be reviewed during a 90-day access review:
  - accounts inactive for 90+ days
  - admin accounts held by people outside the approved admin group
  - accounts of people who have left (status = terminated) but are still enabled
Uses only fake sample data.
"""
import csv
from datetime import date, datetime

INPUT_FILE = "sample_users.csv"
OUTPUT_FILE = "access_review_report.csv"
INACTIVE_DAYS = 90
APPROVED_ADMIN_DEPTS = {"IT Security"}
TODAY = date.today()


def days_since(last_login: str) -> int:
    """Return how many days ago the user last logged in."""
    login_date = datetime.strptime(last_login, "%Y-%m-%d").date()
    return (TODAY - login_date).days


def review_user(user: dict) -> list:
    """Return a list of findings for one user."""
    findings = []
    inactive = days_since(user["last_login"])
    if user["enabled"] == "yes" and user["status"] == "terminated":
        findings.append("Terminated user still enabled - disable now")
    if user["enabled"] == "yes" and inactive >= INACTIVE_DAYS:
        findings.append(f"Inactive {inactive} days - remove or disable")
    if user["role"] == "admin" and user["department"] not in APPROVED_ADMIN_DEPTS:
        findings.append("Admin rights outside approved group - right-size access")
    return findings


def main():
    with open(INPUT_FILE, newline="") as f:
        users = list(csv.DictReader(f))

    flagged = []
    for user in users:
        for finding in review_user(user):
            flagged.append({"username": user["username"],
                            "department": user["department"],
                            "finding": finding})

    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["username", "department", "finding"])
        writer.writeheader()
        writer.writerows(flagged)

    print(f"Reviewed {len(users)} accounts; {len(flagged)} findings.")
    for row in flagged:
        print(f"- {row['username']} ({row['department']}): {row['finding']}")
    print(f"Report saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
