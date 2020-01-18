
import os

def init():
    global config
    config = {
        'hash_type': None,
        'hashes': b"",
        'wordlist': os.path.join(HERE, "static", "wordlists", "rockyou.txt"),
        'device': 'auto',
        'optimized': True,
        'rules': os.path.join(RULES_DIR, "OneRuleToRuleThemAll.rule"),
        'mask': '?a?a?a?a?a?a?a',
    }

HERE = os.path.abspath(os.path.dirname(__file__))
RULES_DIR = os.path.join(HERE, "static", "rules")

try:
    config
except:
    init()
