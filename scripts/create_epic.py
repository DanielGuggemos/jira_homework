import requests
import datetime
import os
import json

email = os.getenv("JIRA_EMAIL")
token = os.getenv("JIRA_API_TOKEN")
base_url = os.getenv("JIRA_BASE_URL")
project = os.getenv("JIRA_PROJECT_KEY")

# Wochennummer
week = datetime.datetime.now().isocalendar()[1]

auth = (email, token)
headers = {"Content-Type": "application/json"}

# 1. Epic erstellen
epic_payload = {
    "fields": {
        "project": {"key": project},
        "summary": f"Woche {week} – Weekly Epic",
        "issuetype": {"name": "Epic"}
    }
}


r = requests.post(f"{base_url}/rest/api/3/issue", json=epic_payload, auth=auth, headers=headers)
# r.raise_for_status()
if r.status_code >= 300:
    print("Error:", r.status_code)
    print(r.text)
    exit(1)

epic_key = r.json()["key"]

print(f"Epic erstellt: {epic_key}")

# 2. Unteraufgaben (Beispiel)
subtasks = [
    "Planung der Woche",
    "Team Sync",
    "Review der offenen Tickets",
    "Blocker klären"
]

for summary in subtasks:
    issue_payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "issuetype": {"name": "Task"},
            "parent": {"key": epic_key}
        }
    }

    r = requests.post(f"{base_url}/rest/api/3/issue", json=issue_payload, auth=auth, headers=headers)
    r.raise_for_status()
    print(f"Task erstellt: {r.json()['key']}")
