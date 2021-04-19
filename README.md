
# How this works
This uses a python tool [watchdog](https://pypi.org/project/watchdog/), which provides the `watchmedo` utility that allows executing a command on file change.

The file `/var/log/kibana/kibana.log` is monitored for changes, and then based on the server log message an action is executed.

Currently that action is to send a Teams message when an alert is logged. It also implements custom tags to show specific action buttons in the Teams message card.
Each message it processes is uniquely identified by its timestamp and cached in a local SQLite3 database because Kibana seems to send the logs repeatedly. Messages
that have been cached are not re-send to Teams.

# Install
This is installed via Ansible, in the `kibana-log-monitor` role. It is run as a service.

# Checking logs
The service logs to `journalctl`, you can look at the logs with `journalctl -u log-monitor`.