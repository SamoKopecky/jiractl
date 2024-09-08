import os
import sys
from enum import Enum

import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

class Transition(Enum):
    IN_PROGRESS = "In Progress"
    BACKLOG = "Backlog"
    DONE = "Done"
    WONT_DO = "WON'T DO"
    PRE_PROD = "Pre-production"
    BLOCKED = "Blocked"
    IN_REVIEW = "In Review"
    TODO = "To Do"

load_dotenv(f"{os.getenv('HOME')}/.config/jiractl/.env")

def get_url(ticket_key: str) -> str:
    return f"https://heurekagroup.atlassian.net/rest/api/latest/issue/{ticket_key}/transitions"

def get_auth() -> HTTPBasicAuth:
    return HTTPBasicAuth(os.getenv("JIRA_USERNAME"), os.getenv("JIRA_TOKEN"))

def get_transition_id_by_name(transition_name: str, ticket_key: str):
    res = requests.get(get_url(ticket_key), auth=get_auth()).json()
    for transition in res["transitions"]:
        if transition["name"] == transition_name:
            return transition["id"]

def set_transition(transition_id: int, ticket_key: str):
    url = get_url(ticket_key)
    res = requests.post(url, auth=get_auth(), json={"transition": {"id": transition_id}})
    return res.status_code

def main():
    ticket_key = sys.argv[2]
    transition_name = Transition(sys.argv[1]).value
    transition_id = get_transition_id_by_name(transition_name, ticket_key)
    print("transition id", transition_id)
    print("status code", set_transition(transition_id, ticket_key))


if __name__ == "__main__":
    main()
