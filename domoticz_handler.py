from log import L
from handler import hue_upnp_super_handler
from domoticz import DomoticzManager


try:
    import settings

    DOMOTICZ_IP = settings.DOMOTICZ_CONFIG['ip']
    DOMOTICZ_PORT = settings.DOMOTICZ_CONFIG['port']
    DOMOTICZ_USERNAME = settings.DOMOTICZ_CONFIG.get('username')
    DOMOTICZ_PASSWORD = settings.DOMOTICZ_CONFIG.get('DOMOTICZ_PASSWORD')

except:
    DOMOTICZ_IP = ""
    DOMOTICZ_PORT = ""
    DOMOTICZ_USERNAME = None
    DOMOTICZ_PASSWORD = None


class DomoticzHueHandler(hue_upnp_super_handler):
    def __init__(self, name, idx):
        super(DomoticzHueHandler, self).__init__(name)
        self.idx = idx
        self.manager = DomoticzManager(ip=DOMOTICZ_IP, username=DOMOTICZ_USERNAME, port=DOMOTICZ_PORT, password=DOMOTICZ_PASSWORD, logger=L)
        self.manager.fetch_switch_list()

    def set_on(self):
        self.manager.set_switch(self.idx, True)

    def set_off(self):
        self.manager.set_switch(self.idx, False)

    def set_bri(self, value):
        pass
