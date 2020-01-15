
import logging
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from .config import config

def Add(command):
    command = command[3:].strip()
    command = command.split(" ")

    if command[0] == "hash":
        if len(command) == 1:
            LOGGER.error("Specify hash in command.")

        else:
            config["hashes"] += command[1].encode()

LOGGER = logging.getLogger(__name__)
ADD_COMPLETER = NestedCompleter({
    'hash': None,
})
