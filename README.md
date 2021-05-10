This uses a python tool [watchdog](https://pypi.org/project/watchdog/), which provides the `watchmedo` utility that allows executing a command on file change.

The file `/var/log/kibana/kibana.log` is monitored for changes, and then based on the server log message an action is executed.

Currently that action is to send a Teams message when an alert is logged. It also implements custom tags to show specific action buttons in the Teams message card.
Each message it processes is uniquely identified by its timestamp and cached in a local SQLite3 database because Kibana seems to repeat the sending of the server log message. Messages
that have been cached will not trigger the action again.

# Install
This is installed via Ansible, in the `kibana-log-monitor` role. It is run as a service.

# Credentials
The credentials are passed in as Environment variables. The exact names can be seen in the `.py` files - look for `os.environ[...]`.

## Production
For production deployment the credentials are set in the `log-monitor.service.j2` file. The file is made a template and configured with the real values during Ansible configuration time.

## Local / development
Locally, you will likely not be using Ansible, nor the `service.j2` file, so all you need to do is make sure the env vars are set before running the scripts.

# Checking logs
The service logs to `journalctl`, you can look at the logs with `journalctl -u log-monitor`.