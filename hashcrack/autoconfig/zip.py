
import logging
import os
import subprocess
from ..config import config, PLATFORM
from ..john import John
from ..common import NamedTemporaryFile
from .. import types

from prompt_toolkit import print_formatted_text as print, HTML

def run():
    
    if not config['hashes'][-22:].startswith(b"PK\005\006"):
        return

    with NamedTemporaryFile(data=config['hashes']) as myzip:

        with John("zip2john.exe" if PLATFORM == "Windows" else "zip2john") as john:
            out = subprocess.check_output([john, myzip], stderr=subprocess.PIPE).strip()

    if b":" not in out:
        print(HTML("<ansiyellow>This zip doesn't appear to be encrypted.</ansiyellow>"))
        return

    hashes = out.split(b"\n")[0]
    
    hashtype = hashes.split(b"$")[1]
    if hashtype != b"pkzip2":
        print(HTML("<ansiyellow>Unhandled zip type of {} discovered. Please submit the following hash and an example binary to https://github.com/bannsec/hashcrack/issues .</ansiyellow>".format(hashtype)))
        print(hashes)
        return

    hashinfo = hashes.split(b"$")[2].split(b"*")

    # This will be 1 2 or 3.  1 is 'partial'. 2 and 3 are full file data (2 is inline, 3 is load from file).
    hash_data_type = hashinfo[2]

    if hashinfo[2] != b"2":
        print(HTML("<ansiyellow>Unhandled zip data type of {} discovered. Please submit the following hash and an example binary to https://github.com/bannsec/hashcrack/issues .</ansiyellow>".format(hash_data_type)))
        print(hashes)
        return

    # Figure out if it's compressed of not
    hash_compression_level = hashinfo[9]

    # Uncompressed
    if hash_compression_level == b"0":
        # PKZIP (Uncompressed)
        hashtype = next(name for name in types.hashcat if types.hashcat[name] == '17210')
        config['hash_type'] = hashtype
        config['hashes'] = b":".join(out.split(b":")[1:])
        print(HTML("<ansigreen>Autoconfigured zip</ansigreen>"))
        return

    else:
        # PKZIP (Compressed)
        hashtype = next(name for name in types.hashcat if types.hashcat[name] == '17200')
        config['hash_type'] = hashtype
        config['hashes'] = b":".join(out.split(b":")[1:])
        print(HTML("<ansigreen>Autoconfigured zip</ansigreen>"))
        return

# hash.split("$")[2].split("*")[9] -- this will designate the compression level
# important to use Compressed or Not Compressed version of pkzip in hashcat

LOGGER = logging.getLogger(__name__)
