
import logging
from prompt_toolkit.completion import WordCompleter, NestedCompleter
from .config import config
import subprocess
import tempfile
import os
from . import types
from .set import Set

class HashCatRunline:
    """Behaves like string but takes care of creating/removing temporary files. Use as "with" statement."""

    def __init__(self, a, flags=None, pipe=False):
        """

        Args:
            a (int): "a" value to use with hashcat
            flags (list, optional): Extra flags to add
            pipe (bool, optional): Is this piped input? If so, we will not put
                in wordlist/mask. default: False
        """

        if not os.path.isfile(config["wordlist"]):
            LOGGER.error("wordlist doesn't exist...")
            return

        if config["hash_type"] is None:
            LOGGER.error("Must set hashtype.")
            return

        self.a = a
        self.flags = flags or []
        self.pipe = pipe

    def __enter__(self):
        self.hashfile = tempfile.NamedTemporaryFile(delete=False)

        self.hashfile.write(config["hashes"])

        runline = ["hashcat", "-a", str(self.a), "-m", types.hashcat[config["hash_type"]]]
        
        if config["device"] == "cpu":
            runline += ["--force", "-D", "1"]
        elif config["device"] == "gpu":
            runline += ["--force", "-D", "2"]

        if config["optimized"]:
            runline.append("-O")

        if self.a == 3:
            wordlist = config['mask']
        else:
            wordlist = config['wordlist']

        runline += self.flags + [self.hashfile.name] 
        
        if not self.pipe:
            runline.append(wordlist)

        # Gotta close here due to Windows not allowing multiple handles
        self.hashfile.close()

        return runline

    def __exit__(self, exception_type, exception_value, traceback):
        os.unlink(self.hashfile.name)


def Crack(command):
    command = command[5:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":

        with HashCatRunline(a=0) as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "rules":
        
        if len(command) > 1:
            Set("set rules " + " ".join(command[1:]))

        with HashCatRunline(a=0, flags=['-r', config['rules']]) as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "brute":

        # Dynamically set mask
        if len(command) > 1:
            config['mask'] = command[1]

        with HashCatRunline(a=3) as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "show":

        with HashCatRunline(a=0, flags=['--show']) as runline:

            try:
                subprocess.run(runline)
            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "kwp":

        with HashCatRunline(a=0, pipe=True) as runline:

            try:
                # Spin up kwp to feed into hashcat
                kwp = subprocess.Popen(["kwp", config['kwp:basechars'], config['kwp:keymaps'], config['kwp:routes'], '-0', '-s', '1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                #kwp.communicate()
                subprocess.run(runline, stdin=kwp.stdout)

                # Clean up kwp
                kwp.terminate()
                kwp.communicate()

            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "prince":

        with HashCatRunline(a=0, pipe=True) as runline:

            try:
                pp = subprocess.Popen(["pp64", "--case-permute", config["wordlist"]], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                subprocess.run(runline, stdin=pp.stdout)

                # Clean up kwp
                pp.terminate()
                pp.communicate()

            except Exception as e:
                LOGGER.error(e)
                print("Be sure you have opencl drivers installed: sudo apt-get -y install ocl-icd-opencl-dev opencl-headers pocl-opencl-icd")

    elif command[0] == "":
        # Default action. Basically, try all things in an order.
        # Note: Default hashcat behavior is to check the pot file first. Once a password is cracked, future runs will simply not take up any cycles.
        Crack("crack wordlist")

        # More efficient but less exhaustive rule list
        Crack("crack rules best64.rule")

        # Brute up to 7 char password
        Crack("crack brute ?a")
        Crack("crack brute ?a?a")
        Crack("crack brute ?a?a?a")
        Crack("crack brute ?a?a?a?a")
        Crack("crack brute ?a?a?a?a?a")
        Crack("crack brute ?a?a?a?a?a?a")
        Crack("crack brute ?a?a?a?a?a?a?a")

        # Maybe keyboard walk?
        Crack("crack kwp")

        # Cracks more but is larger space
        Crack("crack rules OneRuleToRuleThemAll.rule")

        # Last gasp. Try out prince
        Crack("crack prince")


# https://github.com/intel/compute-runtime/blob/master/documentation/Neo_in_distributions.md
# intel-opencl-icd
# https://software.intel.com/en-us/articles/opencl-drivers#latest_CPU_runtime
LOGGER = logging.getLogger(__name__)
CRACK_COMPLETER = NestedCompleter({
    'brute': None,
    'kwp': None,
    'prince': None,
    'rules': None,
    'show': None,
    'wordlist': None,
})
