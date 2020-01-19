
from . import pcap

def autoconfig():
    # Attempt to autoconfig this
    for autoconfig in autoconfigs:
        autoconfig.run()

autoconfigs = [pcap]
