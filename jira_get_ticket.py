import os
import requests
from requests.auth import HTTPBasicAuth
import json

# for help https://developer.atlassian.com/cloud/jira/service-desk/rest/api-group-request

url = "https://autoreduce.atlassian.net/rest/servicedeskapi/request"

username = os.environ["KIBANA_LOG_MONITOR_JIRA_USER"]
password = os.environ["KIBANA_LOG_MONITOR_JIRA_PASSWORD"]
auth = HTTPBasicAuth(username, password)

headers = {"Accept": "application/json", "Content-Type": "application/json"}

# first do a GET to log in
response = requests.get(
    "https://autoreduce.atlassian.net/rest/auth/latest/session",
    headers=headers,
    auth=auth)

print(
    "GET",
    json.dumps(json.loads(response.text),
               sort_keys=True,
               indent=4,
               separators=(",", ": ")))

# now auth works properly and we can see the issue data
response = requests.get(url + "/ARS-28", headers=headers, auth=auth)

print(
    "GET",
    json.dumps(json.loads(response.text),
               sort_keys=True,
               indent=4,
               separators=(",", ": ")))
