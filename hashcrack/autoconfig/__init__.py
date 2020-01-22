
from ..config import config
from . import pcap
from . import shadow
from . import seven_zip
from . import zip
from . import rar

def autoconfig():

    if config['autoconfig']:

        # Attempt to autoconfig this
        for autoconfig in autoconfigs:
            autoconfig.run()

autoconfigs = [
    shadow,    
    pcap,
    seven_zip,
    zip,
    rar,
]
