This uses a python tool [watchdog](https://pypi.org/project/watchdog/), which provides the `watchmedo` utility that allows executing a command on file change.

The file `/var/log/kibana/kibana.log` is monitored for changes, and then based on the server log message an action is executed.

Currently that action is to send a Teams message when an alert is logged. It also implements custom tags to show specific action buttons in the Teams message card.
Each message it processes is uniquely identified by its timestamp and cached in a local SQLite3 database because Kibana seems to repeat the sending of the server log message. Messages
that have been cached will not trigger the action again.

# Install
This is installed via Ansible, in the `kibana-log-monitor` role. It is run as a service. The URL in the repository is empty, but Ansible replaces the line with the real URL which is stored in the vault.

# Checking logs
The service logs to `journalctl`, you can look at the logs with `journalctl -u log-monitor`.