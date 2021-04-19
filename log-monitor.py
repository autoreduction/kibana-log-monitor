#!/usr/bin/python3.6
import requests
import json

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

CUSTOM_TAGS = {"TAG:UPTIME": {
      "@type": "OpenUri",
      "name": "Check Uptime page",
      "targets": [
        { "os": "default", "uri": "https://reduce.isis.cclrc.ac.uk/kibana/app/uptime" }
      ]
    }
}

con = sqlite3.connect("processed.db")
cur = con.cursor()
try:
    cur.execute("""CREATE TABLE processed (timestamp text)""")
    con.commit()
except sqlite3.OperationalError:
    pass

output = subprocess.check_output("""tac /var/log/kibana/kibana.log | grep -m1 '"type":"log"'""", shell=True)
message = json.loads(output)
print("got message", message)

entries = list(cur.execute(f"SELECT COUNT(timestamp) FROM processed WHERE timestamp='{message['@timestamp']}'"))[0][0]

if "Server log" in message["message"] and entries == 0:
    cur.execute(f"INSERT INTO processed VALUES ('{message['@timestamp']}')")
    con.commit()
    print(message["message"])
    data["text"] = message["message"]
    for tag, action in CUSTOM_TAGS.items():
        if tag in message["message"]:
            data["potentialAction"].append(action)
    print(requests.post(URL, json=data))


