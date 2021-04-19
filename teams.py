#!/usr/bin/python3.6
import requests
import json

import jira

# This is a MS Teams webhook which when POSTed to sends a message to the channel where it is activated.
URL = ""

data = {
    "@context": "https://schema.org/extensions",
    "@type": "MessageCard",
    "themeColor": "0072C6",
    "title": "Alert Raised",
    "text": "",
    "potentialAction": []
}

import subprocess
import json
import sqlite3

# Custom tags for which the message's contents are checked. If it contains the tag, it attaches the `potentialAction`
CUSTOM_TAGS = {
    "TAG:UPTIME": {
        "@type":
        "OpenUri",
        "name":
        "Check Uptime page",
        "targets": [{
            "os": "default",
            "uri": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime"
        }]
    }
}


def send(message: str):
    data["text"] = message
    # check if tags are used and add them
    for tag, action in CUSTOM_TAGS.items():
        if tag in message:
            data["potentialAction"].append(action)
    # Send the request to the URL.
    print(requests.post(URL, json=data))
