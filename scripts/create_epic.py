import requests
import datetime
import os

email = os.getenv("JIRA_EMAIL")
token = os.getenv("JIRA_API_TOKEN")
base_url = os.getenv("JIRA_BASE_URL")
project = os.getenv("JIRA_PROJECT_KEY")

week = datetime.datetime.now().isocalendar()[1]

auth = (email, token)
headers = {"Content-Type": "application/json"}

# --- 1. Epic erstellen ---
epic_payload = {
    "fields": {
        "project": {"key": project},
        "summary": f"Woche {week} – Weekly Epic",
        "issuetype": {"name": "Epic"}
    }
}

r = requests.post(f"{base_url}/rest/api/3/issue", json=epic_payload, auth=auth, headers=headers)
if r.status_code >= 300:
    print("Epic-Fehler:", r.status_code)
    print(r.text)
    exit(1)

epic_key = r.json()["key"]
print(f"Epic erstellt: {epic_key}")

# --- 2. Tasks erstellen (in Teamprojekten ohne Epic-Link) ---
tasks = [
    "Wocheneinstieg",
    "Teammeeting vorbereiten",
    "Review der offenen Punkte",
    "Planung nächste Schritte"
]

for summary in tasks:
    task_payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "issuetype": {"name": "Task"}
        }
    }

    r = requests.post(f"{base_url}/rest/api/3/issue", json=task_payload, auth=auth, headers=headers)
    if r.status_code >= 300:
        print("Task-Fehler:", r.status_code)
        print(r.text)
        exit(1)

    print(f"Task erstellt: {r.json()['key']}")
