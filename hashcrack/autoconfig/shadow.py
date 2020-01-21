
import logging
from ..config import config
from .. import types

from prompt_toolkit import print_formatted_text as print, HTML

def run():

    hashtype = None

    for line in config['hashes'].strip().split(b"\n"):
        
        tokens = line.split(b":")

        # Not a shadow file
        if len(tokens) != 9:
            return

        hash = tokens[1].strip(b"*!")

        # Not shadow
        if hash != b"" and not hash.startswith(b"$"):
            return

        if hash.startswith(b"$6$"):
            # sha512crypt $6$, SHA512 (Unix)
            # Since they may change the text name of this
            hashtype = next(name for name in types.hashcat if types.hashcat[name] == '1800')

        elif hash.startswith(b"$5$"):
            # sha256crypt $5$, SHA256 (Unix)
            # Since they may change the text name of this
            hashtype = next(name for name in types.hashcat if types.hashcat[name] == '7400') 

    # If we made it this far, this should be a strong match. Go with it.
    if hashtype is not None:
        config['hash_type'] = hashtype
        print(HTML("<ansigreen>Autoconfigured shadow file</ansigreen>"))

LOGGER = logging.getLogger(__name__)
