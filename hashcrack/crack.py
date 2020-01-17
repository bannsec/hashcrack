
import logging
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from .config import config
import subprocess
import tempfile
import os
from . import types

class HashCatRunline:
    """Behaves like string but takes care of creating/removing temporary files. Use as "with" statement."""

    def __init__(self, flags=None):

        if not os.path.isfile(config["wordlist"]):
            LOGGER.error("wordlist doesn't exist...")
            return

        if config["hash_type"] is None:
            LOGGER.error("Must set hashtype.")
            return

        self.flags = flags or []

    def __enter__(self):
        self.hashfile = tempfile.NamedTemporaryFile()

        self.hashfile.write(config["hashes"])
        self.hashfile.flush()

        # TODO: Run --show when we know they're cracked...
        runline = ["hashcat", "-a", "0", "-m", types.hashcat[config["hash_type"]]]
        
        if config["device"] == "cpu":
            runline += ["--force", "-D", "1"]
        elif config["device"] == "gpu":
            runline += ["--force", "-D", "2"]

        if config["optimized"]:
            runline.append("-O")

        runline += self.flags + [self.hashfile.name, config["wordlist"]]

        return runline

    def __exit__(self, exception_type, exception_value, traceback):
        self.hashfile.close()


def Crack(command):
    command = command[5:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":

        with HashCatRunline() as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "show":

        with HashCatRunline(flags=['--show']) as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "":
        # Default action. Basically, try all things in an order.
        Crack("crack wordlist")


# https://github.com/intel/compute-runtime/blob/master/documentation/Neo_in_distributions.md
# intel-opencl-icd
# https://software.intel.com/en-us/articles/opencl-drivers#latest_CPU_runtime
LOGGER = logging.getLogger(__name__)
CRACK_COMPLETER = NestedCompleter({
    'wordlist': None,
    'show': None,
})
