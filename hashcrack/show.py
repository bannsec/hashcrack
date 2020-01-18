
from prompt_toolkit.completion import WordCompleter
from .config import config

def Show(command):
    command = command[4:].strip()
    command = command.split(" ")

    if command[0] == "wordlist":
        print(config["wordlist"])

    elif command[0] == "hashes":
        print(config["hashes"])

    elif command[0] == "hashtype":
        print(config["hash_type"])

    elif command[0] == "rules":
        print(config["rules"])

    elif command[0] in ["cracked", ""]:
        Crack("crack show")

    elif command[0] == "optimized":
        print(config["optimized"])

    elif command[0] == "mask":
        print(config["mask"])

from .crack import Crack
SHOW_COMPLETER = WordCompleter(['cracked', 'hashes', 'hashtype', 'mask', 'optimized', 'rules', 'wordlist'])