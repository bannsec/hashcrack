
import logging
from hashid import HashID
from .config import config

def Identify(command):
    if config['hashes'] == b"":
        LOGGER.error("Please set a hash first.")
        return

    hid = HashID()

    possible = hid.identifyHash(config["hashes"].split(b"\n")[0].decode())

    print("Possible identifications: " + ",".join(x.name for x in possible))

LOGGER = logging.getLogger(__name__)
