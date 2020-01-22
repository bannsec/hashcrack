
import os
import platform

def init():
    global config
    config = {
        'autoconfig': True,
        'hash_type': None,
        'hashes': b"",
        'wordlist': os.path.join(HERE, "static", "wordlists", "rockyou.txt"),
        'device': 'auto',
        'optimized': True,
        'rules': os.path.join(RULES_DIR, "OneRuleToRuleThemAll.rule"),
        'mask': '?a?a?a?a?a?a?a',
        'kwp:basechars': os.path.join(KWP_BASECHARS_DIR, 'ascii.base'),
        'kwp:keymaps': os.path.join(KWP_KEYMAPS_DIR, 'en.keymap'),
        'kwp:routes': os.path.join(KWP_ROUTES_DIR, '2-to-16-max-3-direction-changes.route'),
    }

HERE = os.path.abspath(os.path.dirname(__file__))
RULES_DIR = os.path.join(HERE, "static", "rules")
KWP_DIR = os.path.join(HERE, "static", "kwp")
KWP_BASECHARS_DIR = os.path.join(KWP_DIR, "basechars")
KWP_KEYMAPS_DIR = os.path.join(KWP_DIR, "keymaps")
KWP_ROUTES_DIR = os.path.join(KWP_DIR, "routes")

PLATFORM = platform.uname().system

try:
    config
except:
    init()
