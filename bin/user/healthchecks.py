#
#    Copyright (c) 2021-2023 Rich Bell <bellrichm@gmail.com>
#
#    See the file LICENSE.txt for your full rights.
#
"""
'ping' healthchecks on every archive record.
See, https://healthchecks.io/docs/

Configuration:
[HealthChecks]
   # Whether the service is enabled or not.
   # Valid values: True or False
   # Default is True.
   # enable = True

    # The host to 'ping'
    # Default is hc-ping.com
    # host = hc-ping.com

    # The HealthChecks uuid
    uuid = REPLACE_ME

    # The http request timeout
    # The default is 10
    # timeout = 10
"""

import logging
import socket
import threading

from urllib.request import urlopen

import weewx
import weeutil.logger
from weewx.engine import StdService
from weewx.reportengine import ReportGenerator

from weeutil.weeutil import to_bool, to_int

VERSION = "0.2.1"

log = logging.getLogger(__name__)
def setup_logging(logging_level, config_dict):
    """ Setup logging for running in standalone mode."""
    if logging_level:
        weewx.debug = logging_level

    weeutil.logger.setup('wee_HealthChecks', config_dict)

def logdbg(msg):
    """ Log debug level. """
    log.debug(msg)

def loginf(msg):
    """ Log informational level. """
    log.info(msg)

def logerr(msg):
    """ Log error level. """
    log.error(msg)

def send_ping(host, uuid, timeout, ping_type=None):
    """Send the HealthChecks 'ping'."""
    if ping_type:
        url = f"https://{host}/{uuid}/{ping_type}"
    else:
        url = f"https://{host}/{uuid}"

    try:
        urlopen(url, timeout=timeout)
    except socket.error as exception:
        logerr(f"Ping failed: {exception}")

class HealthChecksService(StdService):
    """ A service to ping a healthchecks server.. """
    def __init__(self, engine, config_dict):
        super(HealthChecksService, self).__init__(engine, config_dict)

        # service_dict = config_dict.get('HealthChecks', {})
        skin_dict = self.config_dict.get('StdReport', {}).get('HealthChecks', {})

        self.enable = to_bool(skin_dict.get('enable', True))
        if not self.enable:
            loginf("Not enabled, exiting.")
            return

        self.host = skin_dict.get('host', 'hc-ping.com')
        self.timeout = to_int(skin_dict.get('timeout', 10))
        self.uuid = skin_dict.get('uuid')
        if not self.uuid:
            raise ValueError("uuid option is required.")

        self._thread = None

        send_ping(self.host, self.uuid, self.timeout, "start")

        # possible option to run as a service only
        # self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        # self._thread = HealthChecksServiceThread(self.host, self.uuid, self.timeout)
        # self._thread.start()

    def new_archive_record(self, event): # Need to match signature pylint: disable=unused-argument
        """The new archive record event."""
        self._thread.threading_event.set()

    def shutDown(self):
        """Run when an engine shutdown is requested."""
        loginf("SHUTDOWN - initiated")

        send_ping(self.host, self.uuid, self.timeout, "fail")
        loginf("fail ping sent")

        if self._thread:
            loginf("SHUTDOWN - thread initiated")
            self._thread.running = False
            self._thread.threading_event.set()
            self._thread.join(20.0)
            if self._thread.is_alive():
                logerr(f"Unable to shut down {self._thread.name} thread")

            self._thread = None

class HealthChecksServiceThread(threading.Thread):
    """A service to send 'pings' to a HealthChecks server. """
    def __init__(self, host, uuid, timeout):
        threading.Thread.__init__(self)

        self.running = False

        self.host = host
        self.uuid = uuid
        self.timeout = timeout

        self.threading_event = threading.Event()

    def run(self):
        self.running = True

        while self.running:
            self.threading_event.wait()
            send_ping(self.host, self.uuid, self.timeout)
            self.threading_event.clear()

        loginf("exited loop")

class HealthChecksGenerator(ReportGenerator):
    """Class for managing the healthchecks generator."""
    def __init__(self, config_dict, skin_dict, *args, **kwargs):
        """Initialize an instance of HealthChecksGenerator"""
        weewx.reportengine.ReportGenerator.__init__(self, config_dict, skin_dict, *args, **kwargs)

        self.host = skin_dict.get('host', 'hc-ping.com')
        self.timeout = to_int(skin_dict.get('timeout', 10))
        self.uuid = skin_dict.get('uuid')
        if not self.uuid:
            raise ValueError("uuid option is required.")

    def run(self):
        send_ping(self.host, self.uuid, self.timeout)

if __name__ == "__main__":
    pass
