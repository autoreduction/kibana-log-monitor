# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

SERVICES = {
    "TAG:REDUCE": {
        "id":
        "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/27d089ca-a0fd-11eb-be7a-128b42819424"
    },
    "TAG:REDUCESTATIC": {
        "id":
        "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/53493872-a0fd-11eb-9efb-128b42819424"
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

    print(
        "GET",
        json.dumps(json.loads(response.text),
                   sort_keys=True,
                   indent=4,
                   separators=(",", ": ")))

    if "TAG:REDUCE" in message:
        name, service = "reduce.isis.cclrc.ac.uk", SERVICES["TAG:REDUCE"]
    else:
        name, service = "reduce.isis.cclrc.ac.uk static files", SERVICES[
            "TAG:REDUCESTATIC"]

    payload = {
        "serviceDeskId": "1",
        "requestTypeId": "12",
        "requestFieldValues": {
            "summary": name,
            "description": "A server log triggered this incident.",
            "customfield_10036": [service]
        },
    }

    response = requests.post(URL, json=payload, headers=HEADERS, auth=AUTH)

    print(
        "POST",
        json.dumps(json.loads(response.text),
                   sort_keys=True,
                   indent=4,
                   separators=(",", ": ")))
