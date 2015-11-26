from log import L
from handler import hue_upnp_super_handler
from domoticz import DomoticzManager

class DomoticzHueHandler(hue_upnp_super_handler):
    def __init__(self, name, idx, manager):
        super(DomoticzHueHandler, self).__init__(name)
        self.idx = idx
        self.manager = manager
        self.manager.fetch_switch_list()

    def set_on(self):
        self.manager.set_switch(self.idx, True)

    def set_off(self):
        self.manager.set_switch(self.idx, False)

    def set_bri(self, value):
        pass
