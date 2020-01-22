
import logging
import tempfile
import platform
import os
import lzma
import shutil
import tarfile
import sys
import subprocess
from .config import HERE, PLATFORM

class John:

    def __init__(self, name=None):
        """Meant to be used as a "with" statement.
        
        Example:

            # Extracts appropriate john, then removes it
            with John("zip2john.exe") as j:
                subprocess.check_output([j, something])
        """
        self.name = name or "john.exe" # Because nix doesn't care about extensions

    def _enter_windows(self):
        with tarfile.open(os.path.join(HERE, "static", "john.exe.tar.xz"), "r") as src:
            src.extractall(self._dir_path)

        orig = os.path.join(self._dir_path, "john.exe")
        self.path = os.path.join(self._dir_path, self.name)

        os.rename(orig, self.path)

    def _enter_unix(self):
        self.path = os.path.join(self._dir_path, self.name)

        with lzma.open(os.path.join(HERE, "static", "john.xz"), "rb") as src:
            with open(self.path, "wb") as dst:
                dst.write(src.read())

        os.chmod(self.path, 0o500)

    def __enter__(self):

        self._dir_path = tempfile.mkdtemp()

        if platform.uname().system == "Windows":
            self._enter_windows()

        else:
            self._enter_unix()

        return self.path

    def __exit__(self, *args):
        shutil.rmtree(self._dir_path)

#
# Runners for cli bindings 
#

def cli_john():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John() as john:
        subprocess.run([john] + args)

def cli_zip2john():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('zip2john.exe' if PLATFORM == "Windows" else "zip2john") as john:
        subprocess.run([john] + args)

def cli_rar2john():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('rar2john.exe' if PLATFORM == "Windows" else "rar2john") as john:
        subprocess.run([john] + args)

def cli_gpg2john():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('gpg2john.exe' if PLATFORM == "Windows" else "gpg2john") as john:
        subprocess.run([john] + args)

def cli_unafs():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('unafs.exe' if PLATFORM == "Windows" else "unafs") as john:
        subprocess.run([john] + args)

def cli_undrop():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('undrop.exe' if PLATFORM == "Windows" else "undrop") as john:
        subprocess.run([john] + args)

def cli_unshadow():
    args = [] if len(sys.argv) == 1 else sys.argv[1:]
    
    with John('unshadow.exe' if PLATFORM == "Windows" else "unshadow") as john:
        subprocess.run([john] + args)

LOGGER = logging.getLogger(__name__)
