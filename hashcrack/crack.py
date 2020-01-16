
import logging
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from .config import config
import subprocess
import tempfile
import os
from . import types

def Crack(command):
    command = command[5:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":
        if not os.path.isfile(config["wordlist"]):
            LOGGER.error("wordlist doesn't exist...")
            return

        if config["hash_type"] is None:
            LOGGER.error("Must set hashtype.")
            return

        with tempfile.NamedTemporaryFile() as hashfile:
            hashfile.write(config["hashes"])
            hashfile.flush()

            runline = ["hashcat", "--show", "-a", "0", "-m", types.hashcat[config["hash_type"]], hashfile.name, config["wordlist"]]
            subprocess.run(runline)


# https://github.com/intel/compute-runtime/blob/master/documentation/Neo_in_distributions.md
# intel-opencl-icd
# https://software.intel.com/en-us/articles/opencl-drivers#latest_CPU_runtime
LOGGER = logging.getLogger(__name__)
CRACK_COMPLETER = NestedCompleter({
    'wordlist': None,
})
