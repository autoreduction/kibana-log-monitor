# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://autoreduce.atlassian.net/rest/api/3/issue"

auth = HTTPBasicAuth("email", "api token")

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}
response = requests.get("https://autoreduce.atlassian.net/rest/auth/latest/session",
   headers=headers,
   auth=auth
)
print("GET", json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

payload = {
  "update": {},
  "fields": {
    "summary": "Main order flow broken",
    # "parent": {
    #   "key": "ARS"
    # },
    "issuetype": {
      "id": "10001"
    },
    "project": {
      "id": "10000"
    },
    # "description": {
    #   "type": "doc",
    #   "version": 1,
    #   "content": [
    #     {
    #       "type": "paragraph",
    #       "content": [
    #         {
    #           "text": "Order entry fails when selecting supplier.",
    #           "type": "text"
    #         }
    #       ]
    #     }
    #   ]
    # },
    # "environment": {
    #   "type": "doc",
    #   "version": 1,
    #   "content": [
    #     {
    #       "type": "paragraph",
    #       "content": [
    #         {
    #           "text": "UAT",
    #           "type": "text"
    #         }
    #       ]
    #     }
    #   ]
    # },
    # "versions": [
    #   {
    #     "id": "10000"
    #   }
    # ],
  }
}

response = requests.post(url,
   json=payload,
   headers=headers,
   auth=auth
)

print("POST",json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))