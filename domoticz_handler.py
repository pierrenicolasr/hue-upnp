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
        return self.manager.change_switch_state(self.idx, True) == 'OK'

    def set_off(self):
        return self.manager.change_switch_state(self.idx, False) == 'OK'

    def set_bri(self, value):
        return self.manager.change_switch_state(self.idx, True) == 'OK'
