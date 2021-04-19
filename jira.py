# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

SERVICES = {
    "TAG:REDUCE": {
        "name": "Host reduce.isis.cclrc.ac.uk is not responding",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime",
        "jira_field": {
            "id":
            "ari:cloud:graph::run/b0a0787a-e104-460d-ad03-f976135c8a6a/27d089ca-a0fd-11eb-be7a-128b42819424"
        }
    },
    "TAG:REDUCESTATIC": {
        "name":
        "Host of reduce.isis.cclrc.ac.uk static files is not responding",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime",
        "jira_field": {
            "id":
            "ari:cloud:graph::run/b0a0787a-e104-460d-ad03-f976135c8a6a/53493872-a0fd-11eb-9efb-128b42819424"
        }
    },
    "TAG:ACTIVEMQSTALE": {
        "name": "Stale messages in ActiveMQ",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana",
        "jira_field": {
            "id":
            "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/63e707a4-a0fd-11eb-9118-128b42819424"
        }
    },
    "TAG:QUEUEPROCESSORS": {
        "name":
        "Something gone wrong with queue processors (this isn't used yet)",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana",
        "jira_field": {
            "id":
            "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/6a3d6a58-a0fd-11eb-be82-128b42819424"
        }
    },
    "OTHER": {
        "name": "unknown service",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime",
        "jira_field": ""
    }
}

# for help https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request

URL = "https://autoreduce.atlassian.net/rest/servicedeskapi/request"

AUTH = HTTPBasicAuth("", "")

HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def send(message: str):
    response = requests.get(
        "https://autoreduce.atlassian.net/rest/auth/latest/session",
        headers=HEADERS,
        auth=AUTH)

    print("GET", json.dumps(json.loads(response.text), sort_keys=True))

    tag = "OTHER"
    for key in SERVICES.keys():
        if key in message:
            tag = key
            break

    payload = {
        "serviceDeskId": "1",
        "requestTypeId": "12",
        "requestFieldValues": {
            "summary": f"Disruption: {SERVICES[tag]['name']}",
            "description":
            f"A server log triggered this incident. Check {SERVICES[tag]['link']} for more info",
            "customfield_10036": [SERVICES[tag]['jira_field']]
        },
    }

    response = requests.post(URL, json=payload, headers=HEADERS, auth=AUTH)

    print("POST", json.dumps(json.loads(response.text), sort_keys=True))
