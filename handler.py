from log import L


#
# This is the main object which all other handlers inherit from:
class hue_upnp_super_handler(object):
    def __init__(self, name):
        self.name = name
        self.on = "true"
        self.bri = 254
        self.xy = [0.0, 0.0]
        self.ct = 201

    # Set default initial values
    # Can be overridden, or used as a super, or just use the defaults.
    def get_all(self):
        self.on = "true"
        self.bri = 254
        self.xy = [0.0, 0.0]
        self.ct = 201

    # Super set method, parses incomming data and runs the appropriate method.
    def set(self, data):
        ret = False
        # TODO: If bri is specified, we only call set_bri and ignore on, is that the right thing?
        # TODO: I think so, because it's up to the bri method to know what to do.
        if 'bri' in data:
            # For some reason, the first time on/off is toggled from harmony it passes on: true, bri: 0
            # so we assume it really meant full on...
            if 'on' in data and data['on'] and data['bri'] == 0:
                ret = self.set_on()
            else:
                ret = self.set_bri(data['bri'])
            if ret:
                self.on = "true"
                self.bri = data['bri']
        elif 'on' in data:
            if data['on']:
                ret = self.set_on()
                if ret:
                    self.on = "true"
            else:
                ret = self.set_off()
                if ret:
                    self.on = "false"
        else:
            L.error("ERROR: Unknown set data: " + data)
        return ret

    # Default, should always be overridden
    def set_on(self):
        L.error("ERROR: Device " + self.name + " does not have an on command?")

    # Default, should always be overridden
    def set_off(self):
        L.error("ERROR: Device " + self.name + " does not have an off command?")

    # Default, should always be overridden
    def set_bri(self, value):
        L.error("ERROR: Device " + self.name + " does not have a bri command?")

    # Default, should always be overridden
    def set_ct(self, value):
        L.error("ERROR: Device " + self.name + " does not have a ct command?")

    # Default, should always be overridden
    def set_xy(self, value):
        L.error("ERROR: Device " + self.name + " does not have a xy command?")
