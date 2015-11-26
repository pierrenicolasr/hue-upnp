# from shell_handler import hue_upnp_shell_handler
from domoticz_handler import DomoticzHueHandler
from domoticz import DomoticzManager
from log import L

IP = "192.168.1.135"  # Callback http webserver IP (this machine)
HTTP_PORT = 8085  # HTTP-port to serve icons, xml, json (80 is most compatible but requires root)
GATEWAYIP = "192.168.1.254"  # shouldn't matter but feel free to adjust
MACADDRESS = "b8:27:eb:06:9d:18"  # shouldn't matter but feel free to adjust
DEBUG = False

# If using the ISY calls, set your info here:
ISY_CONFIG = {
    'ip': '192.168.1.xxx',
    'username': 'your_user_name',
    'password': 'your_password'
}

DOMOTICZ_CONFIG = {
    'ip': '192.168.1.5',
    'port': '8080',
    # 'username': 'your_user_name',
    # 'password': 'your_password'
}

# sets your devices
domoticx_cfg = dict(logger=L)
domoticx_cfg.update(DOMOTICZ_CONFIG)

mgr = DomoticzManager(**domoticx_cfg)

exclude_subtypes = ('KD101 smoke detector',)
exclude_descriptions = ('[exclude_harmony]',)
exclude_hardware_types = ('Logitech Harmony Hub','Kodi Media Server')

def get_devices():
    mgr.fetch_switch_list()


    ret = []
    for light in mgr.get_light_details():
        if x.get('SubType') in exclude_subtypes:
            continue
        if x.get('Description') in exclude_descriptions:
            continue
        if x.get('HardwareType') in exclude_hardware_types:
            continue
        ret.append(
            DomoticzHueHandler(
                light.name,
                light.idx,
                mgr
            )
        )
    return ret