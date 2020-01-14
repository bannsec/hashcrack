
import os
import logging
from prompt_toolkit.completion import Completer, Completion, NestedCompleter, PathCompleter, WordCompleter
from .config import config
from . import types

def Set(command):
    command = command[3:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":
        wordlist = os.path.abspath(" ".join(command[1:]))
        if os.path.isfile(wordlist):
            config["wordlist"] = wordlist
        else:
            LOGGER.error("Does not appear to be a valid file...")

    elif command[0] == "hashfile":
        hashfile = os.path.abspath(" ".join(command[1:]))
        if os.path.isfile(hashfile):
            with open(hashfile, "rb") as f:
                config["hashes"] += f.read()
        else:
            LOGGER.error("Does not appear to be a valid file...")

    elif command[0] == "hashtype":
        hashtype = " ".join(command[1:])
        if hashtype not in types.hashcat:
            LOGGER.error("Not a valid hash type.")
        else:
            config["hash_type"] = hashtype

LOGGER = logging.getLogger(__name__)

SET_COMPLETER = NestedCompleter({
    "wordlist": PathCompleter(),
    "hashfile": PathCompleter(),
    "hashtype": WordCompleter(types.hashcat.keys(), ignore_case=True, match_middle=True),
})
