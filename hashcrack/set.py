
import os
import logging
from prompt_toolkit.completion import Completer, Completion, NestedCompleter, PathCompleter, WordCompleter
from .config import config, RULES_DIR
from . import types

def Set(command):
    command = command[3:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":
        wordlist = os.path.abspath(" ".join(command[1:]))
        if os.path.isfile(wordlist):
            config["wordlist"] = wordlist
        else:
            LOGGER.error("Wordlist does not appear to be a valid file...")

    elif command[0] == "hashfile":
        hashfile = os.path.abspath(" ".join(command[1:]))
        if os.path.isfile(hashfile):
            with open(hashfile, "rb") as f:
                config["hashes"] += f.read()
        else:
            LOGGER.error("Hashfile does not appear to be a valid file...")

    elif command[0] == "hashtype":
        hashtype = " ".join(command[1:])
        if hashtype not in types.hashcat:
            LOGGER.error("Not a valid hash type.")
        else:
            config["hash_type"] = hashtype

    elif command[0] == "device":

        if command[1] not in ["auto", "gpu", "cpu"]:
            LOGGER.error("Valid device types: auto, gpu, cpu.")
            return
        
        config['device'] = command[1]

    elif command[0] == "optimized":

        if command[1] not in ["true", "false"]:
            LOGGER.error("Valid optimized flags are: true, false")
            return

        config["optimized"] = True if command[1] == "true" else False

    elif command[0] == "rules":
        rulesfile = " ".join(command[1:])

        if not os.path.isabs(rulesfile):
            rulesfile = os.path.abspath(os.path.join(RULES_DIR, rulesfile))

        if os.path.isfile(rulesfile):
            config["rules"] = rulesfile
        else:
            LOGGER.error("Can't find rules file at " + rulesfile)

    elif command[0] == "mask":
        if len(command) == 1:
            print(MASK_HELP)
            return

        mask = " ".join(command[1:])
        config['mask'] = mask

LOGGER = logging.getLogger(__name__)

SET_COMPLETER = NestedCompleter({
    "device": WordCompleter(["auto", "cpu", "gpu"]),
    "hashfile": PathCompleter(),
    "hashtype": WordCompleter(types.hashcat.keys(), ignore_case=True, match_middle=True),
    "mask": None,
    "optimized": WordCompleter(["true", "false"]),
    "rules": PathCompleter(get_paths=lambda:[RULES_DIR]),
    "wordlist": PathCompleter(),
})

MASK_HELP = r"""usage: set mask <mask_here>

Default mask charsets:
    ?l = abcdefghijklmnopqrstuvwxyz
    ?u = ABCDEFGHIJKLMNOPQRSTUVWXYZ
    ?d = 0123456789
    ?h = 0123456789abcdef
    ?H = 0123456789ABCDEF
    ?s = «space»!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    ?a = ?l?u?d?s
    ?b = 0x00 - 0xff

Example:
    Brute force 7 char password: ?a?a?a?a?a?a?a
"""
