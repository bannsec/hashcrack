
import logging
from ..config import config
from scapy.all import *
import io
import tempfile
import subprocess
import os

from prompt_toolkit import print_formatted_text as print, HTML

def run():

    pcap_headers = [b'\xa1\xb2\xc3\xd4', b'\xd4\xc3\xb2\xa1', b'\xa1\xb2\xcd4', b'\n\r\r\n`\x00\x00\x00M<+\x1a']

    # Using scapy to standardize the output. This is probably only required for
    # pcapng, since cap2hccapx doesn't accept that format
    if any(config['hashes'].startswith(header) for header in pcap_headers):

        LOGGER.info("Discovered pcapng file.")

        # Use scapy to change format
        packets = rdpcap(io.BytesIO(config['hashes']))
        out = io.BytesIO()
        # Gotta remove close or we won't be able to read it
        out.close = lambda:1

        # Write to temp file so we can call cap2hccapx
        # NO delete due to windows file handle issues
        temp = tempfile.NamedTemporaryFile(delete=False)
        wrpcap(temp, packets) # This will close the file

        temp_out = tempfile.NamedTemporaryFile(delete=False)
        temp_out.close()
        
        subprocess.check_output(["cap2hccapx", temp.name, temp_out.name])
        
        # Suck up the new info
        with open(temp_out.name, "rb") as f:
            config['hashes'] = f.read()

        # Guessing at the protocol for now.
        # TODO: Use scapy to guess better
        config['hash_type'] = 'WPA-EAPOL-PBKDF2'
        print(HTML("<ansigreen>Autoconfigured pcap</ansigreen>"))

        # Clean-up temp files
        os.unlink(temp.name)
        os.unlink(temp_out.name)


LOGGER = logging.getLogger(__name__)
