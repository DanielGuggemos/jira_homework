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

# --- 1. Weekly Task erstellen ---
task_payload = {
    "fields": {
        "project": {"key": project},
        "summary": f"Woche {week} – Weekly Task",
        "issuetype": {"name": "Task"}
    }
}

r = requests.post(f"{base_url}/rest/api/3/issue", json=task_payload, auth=auth, headers=headers)
if r.status_code >= 300:
    print("Task-Fehler:", r.status_code)
    print(r.text)
    exit(1)

parent_key = r.json()["key"]
print(f"Task erstellt: {parent_key}")

# --- 2. Sub‑Tasks erstellen ---
subtasks = [
    "Treppenaus saugen 1",
    "Treppenaus saugen 2",
    "Bad und Klo putzen",
    "Küche und Gang saugen 1",
    "Küche und Gang saugen 2",
    "Küche und Gang saugen 3",
]

for summary in subtasks:
    sub_payload = {
        "fields": {
            "project": {"key": project},
            "summary": summary,
            "issuetype": {"name": "Sub-task"},
            "parent": {"key": parent_key}
        }
    }

    r = requests.post(f"{base_url}/rest/api/3/issue", json=sub_payload, auth=auth, headers=headers)
    if r.status_code >= 300:
        print("Subtask-Fehler:", r.status_code)
        print(r.text)
        exit(1)

    print(f"Subtask erstellt: {r.json()['key']}")


