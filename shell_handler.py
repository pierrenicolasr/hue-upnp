from handler import hue_upnp_super_handler
import subprocess


class hue_upnp_shell_handler(hue_upnp_super_handler):
    def __init__(self, name, program):
        super(hue_upnp_shell_handler, self).__init__(name)
        self.program = program

    def set_on(self):
        # Use external program to do "stuff" if desired
        return subprocess.Popen([self.program, self.name, "on", "true"])

    def set_off(self):
        # Use external program to do "stuff" if desired
        return subprocess.Popen([self.program, self.name, "on", "false"])

    def set_bri(self, value):
        # Use external program to do "stuff" if desired
        subprocess.Popen([self.program, self.name, "bri", str(value)])

    def set_ct(self, value):
        # Use external program to do "stuff" if desired
        subprocess.Popen([self.program, self.name, "ct", value])

    def set_xy(self, value):
        # Use external program to do "stuff" if desired
        subprocess.Popen([self.program, self.name, "xy", value])
