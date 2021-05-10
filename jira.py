import os
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
        "name": "The number of live ActiveMQ consumers is 0!",
        "link": "https://reduce.isis.cclrc.ac.uk/kibana",
        "jira_field": {
            "id":
            "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/6a3d6a58-a0fd-11eb-be82-128b42819424"
        }
    },
    "TAG:ELASTICSEARCHDISK": {
        "name": "Elasticsearch host node is running low on disk space",
        "link":
        r"https://reduce.isis.cclrc.ac.uk/kibana/app/metrics/explorer?metricsExplorer=(chartOptions:(stack:!f,type:line,yAxisMode:fromZero),options:(aggregation:avg,filterQuery:%27host.name:%20%22elasticsearch%22%20%27,metrics:!((aggregation:avg,color:color0,field:system.filesystem.available),(aggregation:avg,color:color1,field:system.filesystem.free)),source:default),timerange:(from:now-10m,interval:%3E%3D10s,to:now))&waffleFilter=(expression:%27%27,kind:kuery)&waffleTime=(currentTime:1618913625590,isAutoReloading:!f)&waffleOptions=(accountId:%27%27,autoBounds:!t,boundsOverride:(max:1,min:0),customMetrics:!(),customOptions:!(),groupBy:!(),legend:(palette:cool,reverseColors:!f,steps:10),metric:(type:cpu),nodeType:host,region:%27%27,sort:(by:name,direction:desc),source:default,view:map)",
        "jira_field": {
            "id":
            "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/af43def6-a1c1-11eb-b065-128b42819424"
        }
    },
    "TAG:DATABASEBACKUP": {
        "name":
        "The last database backup did not restore correctly. Check db-backup node.",
        "link": "",
        "jira_field": {
            "id":
            "ari:cloud:graph::service/b0a0787a-e104-460d-ad03-f976135c8a6a/fbb6a7da-a2a9-11eb-8449-128b42819424"
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

username = os.environ["KIBANA_LOG_MONITOR_JIRA_USER"]
password = os.environ["KIBANA_LOG_MONITOR_JIRA_PASSWORD"]
AUTH = HTTPBasicAuth(username, password)

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


if __name__ == "__main__":
    import sys
    send(sys.argv[1])
