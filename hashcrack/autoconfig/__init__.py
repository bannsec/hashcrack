
from ..config import config
from . import pcap
from . import shadow

def autoconfig():

    if config['autoconfig']:

        # Attempt to autoconfig this
        for autoconfig in autoconfigs:
            autoconfig.run()

autoconfigs = [
    shadow,    
    pcap,
]
