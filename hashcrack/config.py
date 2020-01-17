
import os

def init():
    global config
    config = {
        'hash_type': None,
        'hashes': b"",
        'wordlist': os.path.join(HERE, "static", "wordlists", "rockyou.txt"),
        'device': 'auto',
        'optimized': True,
    }

HERE = os.path.abspath(os.path.dirname(__file__))

try:
    config
except:
    init()
