import requests
from requests.auth import HTTPBasicAuth
import logging
import logging.handlers
import sys
import json


class Light(object):
    def __init__(self, sub_type, idx, type, name, is_dimmer, manager=None):
        self.sub_type = sub_type
        self.idx = idx
        self.type = type

        # convert to ascii for now
        self.name=name.encode("ascii","ignore")
        self.is_dimmer = is_dimmer
        self.manager = manager

    @classmethod
    def from_dict(cls, dict, manager=None):
        # convert to ascii for now
        name=dict.get('Name', '').encode("ascii","ignore")
        return Light(
            sub_type=dict.get('SubType'),
            idx=dict.get('idx'),
            type=dict.get('Type'),
            name=name,
            is_dimmer=dict.get('IsDimmer'),
            manager=manager,
        )

    def turn_on(self):
        if self.manager:
            return self.manager.change_switch_state(self.idx, True)

    def turn_off(self):
        if self.manager:
            self.manager.change_switch_state(self.idx, False)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return u"Light_%s_%s" % (self.idx, self.name)

    def __repr__(self):
        return u"Light_%s_%s" % (self.idx, self.name)


class DomoticzManager(object):

    def __init__(self, ip, port, username=None, password=None, logger=None):
        self.ip = ip
        self.port = port
        self.username = username
        self.password=password
        self.auth = HTTPBasicAuth(username, password) if self.username else None
        self.logger = logger or self._default_logger()
        self.lights = {}
        self.fetch_switch_list()


    @staticmethod
    def _default_logger():
        logFormatter = logging.Formatter("[domoticz] %(asctime)s [%(levelname)-5.5s] %(message)s")
        log = logging.getLogger()
        log.setLevel(logging.INFO)
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        log.addHandler(consoleHandler)
        return log

    def _request(self, arguments):
        url = "http://{}:{}/json.htm".format(self.ip, self.port)
        r = requests.get(
            url=url,
            params=arguments,
            auth=self.auth
        )
        if not r.status_code == 200:
            self.logger.error("Error contacting domoticz : %d-%s", r.status_code, r.content)

        try:
            ret = json.loads(r.content)
        except TypeError:
            self.logger.error("Error parsing domoticz answer: %s", r.content)
            return None

        if ret.get('status') != 'OK':
            self.logger.error("Domoticz status error: %s", ret.get('status'))

        return ret.get('result')

    def get_device_details(self, idx):
        arguments= {
            'type':'devices',
            'rid':idx
        }
        return self._request(arguments)

    def get_light_details(self):
        arguments= {
            'type':'devices',
            'filter':'light',
            'used':True,
            'order':'Name',
        }
        return self._request(arguments)

    def fetch_switch_list(self):
        self.lights = {
            light.idx : light for light in self.get_switches()
        }

    def get_switches(self):
        arguments = {
            'type':'command',
            'param': 'getlightswitches',
        }
        raw = self._request(arguments)
        return [Light.from_dict(item, self) for item in raw]

    def change_switch_state(self, light_idx, on):
        return self._request(
            arguments={
                'type':'command',
                'param':'switchlight',
                'idx': light_idx,
                'switchcmd': 'On' if on else 'Off',
            }
        )

    def get_light_by_name(self, name):
        for light in self.lights.values():
            if light.name == name:
                return light
