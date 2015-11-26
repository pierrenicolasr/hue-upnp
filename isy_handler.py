from log import L
from handler import hue_upnp_super_handler
from requests.auth import HTTPBasicAuth
import requests

try:
    import settings

    ISY_IP = settings.ISY_CONFIG['ip']
    ISY_USERNAME = settings.ISY_CONFIG['username']
    ISY_PASSWORD = settings.ISY_CONFIG['password']

except:
    ISY_IP = ""
    ISY_USERNAME = ""
    ISY_PASSWORD = ""


class isy_rest_handler(hue_upnp_super_handler):
    def __init__(self, name, address):
        self.address = address
        self.on_cmd = 'http://' + ISY_IP + '/rest/nodes/%s/cmd/DON' % self.address
        self.off_cmd = 'http://' + ISY_IP + '/rest/nodes/%s/cmd/DOF' % self.address
        self.st_cmd = 'http://' + ISY_IP + '/rest/nodes/%s/ST' % self.address
        self.auth = HTTPBasicAuth(ISY_USERNAME, ISY_PASSWORD)
        super(isy_rest_handler, self).__init__(name)

    def get_all(self):
        # Set all the defaults
        super(isy_rest_handler, self).get_all()
        # Query the ISY to get the current values.
        L.debug('ST: ' + self.st_cmd);
        # TODO: Parse the values.
        r = requests.get(self.st_cmd, auth=self.auth)
        return r.status_code == 200

    def set_on(self):
        return self.do_rest(self.on_cmd)

    def set_off(self):
        return self.do_rest(self.off_cmd)

    def set_bri(self, value):
        cmd = self.on_cmd + "/" + str(value)
        return self.do_rest(cmd)

    def do_rest(self, rest):
        L.info("ISY REST: " + rest)
        r = requests.get(rest, auth=self.auth)
        if r.status_code == 200:
            self.on = "true"
            return True
        return False
