#!/usr/bin/python3.6
import requests
import json

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
CUSTOM_TAGS = {"TAG:UPTIME": {
      "@type": "OpenUri",
      "name": "Check Uptime page",
      "targets": [
        { "os": "default", "uri": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime" }
      ]
    }
}

# Set up the SQLite3 db
con = sqlite3.connect("processed.db")
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE processed (timestamp text)""")
    con.commit()
except sqlite3.OperationalError:
    pass

# Get the last message with `tac` (print file backwards) and `grep -m1` (stop on first match)
output = subprocess.check_output("""tac /var/log/kibana/kibana.log | grep -m1 '"type":"log"'""", shell=True)
message = json.loads(output)
print("got message", message)

# Find previously cached messages with the same @timestamp value. Kibana may repeat the messages in the logs
# but they all have the same @timestamp
entries = list(cur.execute(f"SELECT COUNT(timestamp) FROM processed WHERE timestamp='{message['@timestamp']}'"))[0][0]

# Kibana prepends "Server log" in alerts specifically raised to the server log connector
# If entires is not 0 then this message has been processed before, so it is skippped
if "Server log" in message["message"] and entries == 0:
    # cache the message into the db
    cur.execute(f"INSERT INTO processed VALUES ('{message['@timestamp']}')")
    con.commit()
    print(message["message"])
    data["text"] = message["message"]
    # check if tags are used and add them
    for tag, action in CUSTOM_TAGS.items():
        if tag in message["message"]:
            data["potentialAction"].append(action)
    # Send the request to the URL.
    print(requests.post(URL, json=data))


