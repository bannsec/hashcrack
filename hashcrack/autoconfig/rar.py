
import logging
import subprocess
from ..config import config, HERE, PLATFORM
from ..common import NamedTemporaryFile
from ..john import John
from .. import types

from prompt_toolkit import print_formatted_text as print, HTML

def run():

    if not config["hashes"].startswith(b'Rar!\x1a\x07'):
        return

    with NamedTemporaryFile(data=config['hashes']) as myrar:

        with John("rar2john.exe" if PLATFORM == "Windows" else "rar2john") as john:
            out = subprocess.check_output([john, myrar], stderr=subprocess.PIPE).strip()

    if b":" not in out:
        print(HTML("<ansiyellow>This rar doesn't appear to be encrypted.</ansiyellow>"))
        return

    hashes = out.split(b"\n")[0]

    hashtype = hashes.split(b"$")[1]

    if hashtype.lower() == b"rar5":
        # RAR5
        hashtype = next(name for name in types.hashcat if types.hashcat[name] == '13000')
        config['hash_type'] = hashtype
        config['hashes'] = b":".join(out.split(b":")[1:])
        print(HTML("<ansigreen>Autoconfigured rar</ansigreen>"))

    elif hashtype.lower()== b"rar3":

        enctype = hashes.split(b"$")[2].split(b"*")[1]

        # RAR3-hp
        if enctype == b"0":
            hashtype = next(name for name in types.hashcat if types.hashcat[name] == '12500')
            config['hash_type'] = hashtype
            config['hashes'] = b":".join(out.split(b":")[1:])
            print(HTML("<ansigreen>Autoconfigured rar</ansigreen>"))

        elif enctype == b"1":
            print(HTML("<ansired>Hashcat current does not support rar -p (rar3) hashes.</ansired>"))
            return

        else:
            print(HTML("<ansired>Unexpected rar3 type of {} discovered. Please submit the following hash and an example binary to https://github.com/bannsec/hashcrack/issues .</ansired>".format(enctype)))
            print(hashes)
            return

    else:
        print(HTML("<ansiyellow>Unhandled rar type of {} discovered. Please submit the following hash and an example binary to https://github.com/bannsec/hashcrack/issues .</ansiyellow>".format(hashtype)))
        print(out)

LOGGER = logging.getLogger(__name__)
