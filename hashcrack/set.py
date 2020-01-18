
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

LOGGER = logging.getLogger(__name__)

SET_COMPLETER = NestedCompleter({
    "wordlist": PathCompleter(),
    "hashfile": PathCompleter(),
    "hashtype": WordCompleter(types.hashcat.keys(), ignore_case=True, match_middle=True),
    "device": WordCompleter(["auto", "cpu", "gpu"]),
    "optimized": WordCompleter(["true", "false"]),
    "rules": PathCompleter(get_paths=lambda:[RULES_DIR]),
})
