
import os
import logging
from prompt_toolkit.completion import Completer, Completion, NestedCompleter, PathCompleter, WordCompleter
from .config import config, RULES_DIR, KWP_BASECHARS_DIR, KWP_KEYMAPS_DIR, KWP_ROUTES_DIR
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
        # Try to autoconfig it
        autoconfig()

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

    elif command[0] == "kwp:basechars":
        basecharsfile = " ".join(command[1:])

        if not os.path.isabs(basecharsfile):
            basecharsfile = os.path.abspath(os.path.join(KWP_BASECHARS_DIR, basecharsfile))

        if os.path.isfile(basecharsfile):
            config["kwp:basechars"] = basecharsfile
        else:
            LOGGER.error("Can't find basechars file at " + basecharsfile)

    elif command[0] == "kwp:keymaps":
        keymapsfile = " ".join(command[1:])

        if not os.path.isabs(keymapsfile):
            keymapsfile = os.path.abspath(os.path.join(KWP_KEYMAPS_DIR, keymapsfile))

        if os.path.isfile(keymapsfile):
            config["kwp:keymaps"] = keymapsfile
        else:
            LOGGER.error("Can't find keymaps file at " + keymapsfile)

    elif command[0] == "kwp:routes":
        routesfile = " ".join(command[1:])

        if not os.path.isabs(routesfile):
            routesfile = os.path.abspath(os.path.join(KWP_ROUTES_DIR, routesfile))

        if os.path.isfile(routesfile):
            config["kwp:routes"] = routesfile
        else:
            LOGGER.error("Can't find routes file at " + routesfile)

from .autoconfig import autoconfig

LOGGER = logging.getLogger(__name__)

SET_COMPLETER = NestedCompleter({
    "device": WordCompleter(["auto", "cpu", "gpu"]),
    "hashfile": PathCompleter(),
    "hashtype": WordCompleter(types.hashcat.keys(), ignore_case=True, match_middle=True),
    "kwp:basechars": PathCompleter(get_paths=lambda:[KWP_BASECHARS_DIR]),
    "kwp:keymaps": PathCompleter(get_paths=lambda:[KWP_KEYMAPS_DIR]),
    "kwp:routes": PathCompleter(get_paths=lambda:[KWP_ROUTES_DIR]),
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
