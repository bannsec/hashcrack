
import os
import lzma
import logging
import subprocess
import platform
import tempfile
from .. import types
from ..config import config

from prompt_toolkit import print_formatted_text as print, HTML

"""
Using: https://github.com/philsmd/7z2hashcat
pp: PAR::Packer -- https://github.com/rschupp/PAR-Packer
Linux: gzexe
    pp -o 7z2hashcat 7z2hashcat.pl
Windows: strawberry perl
    pp -M Compress::Raw::Lzma --link liblzma-5__.dll -o 7z2hashcat.exe 7z2hashcat.pl
"""

def Windows():

    out = b""

    #
    # Uncompress the bin
    #

    fd, sz2hashcat_exe = tempfile.mkstemp(suffix='.exe')

    with lzma.open(os.path.join(HERE, '7z2hashcat.exe.xz'), "rb") as src:
        os.write(fd, src.read())

    os.close(fd)

    #
    # Write out the 7z
    #
    
    tmp7z_fd, tmp7z_name = tempfile.mkstemp(suffix='.7z')
    os.write(tmp7z_fd, config["hashes"])
    os.close(tmp7z_fd)

    #
    # Run the bin
    #
    
    try:
        out = subprocess.check_output([sz2hashcat_exe, tmp7z_name])
    except subprocess.CalledProcessError:
        pass

    #
    # Clean-up
    #

    os.unlink(sz2hashcat_exe)
    os.unlink(tmp7z_name)

    return out


def Unix():

    with tempfile.NamedTemporaryFile(suffix='.7z') as tmp:

        tmp.write(config['hashes'])
        tmp.flush()

        try:
            return subprocess.check_output([os.path.join(HERE, "7z2hashcat"), tmp.name]).strip()
        except subprocess.CalledProcessError:
            pass

def run():
    magic = b"7z\274\257\047\034"

    if not config['hashes'].startswith(magic):
        return

    if platform.uname().system == "Windows":
        out = Windows()

    else:
        out = Unix()

    if out.startswith(b"$7z$"):
        config['hashes'] = out.strip()
        hashtype = next(name for name in types.hashcat if types.hashcat[name] == '11600')
        config['hash_type'] = hashtype

        print(HTML("<ansigreen>Autoconfigured 7zip</ansigreen>"))

HERE = os.path.abspath(os.path.dirname(__file__))
LOGGER = logging.getLogger(__name__)
