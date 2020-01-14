
import os
import lzma
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion, NestedCompleter

here = os.path.abspath(os.path.dirname(__file__))

STYLE = Style.from_dict({
    # User input (default text).
    '':          '#8e89cb',

    # Prompt.
    'hashcrack':  '#89a3cb',
    'white':   '#ffffff',
})

def main():
    setup()
    
    prompt = [
            ('class:hashcrack', 'hashcrack'),
            ('class:white', ' > ')
    ]

    session = PromptSession(prompt, style=STYLE, completer=HashCrackCompleter(), complete_while_typing=True)

    while True:

        try:
            out = session.prompt()
        except (KeyboardInterrupt, EOFError):
            return

        try:
            MENU_FIRST_LEVEL[out.split(" ")[0]]["do"](out)
        except KeyError:
            print("Invalid option.")

def setup():
    rockyou_path = os.path.join(here, "static", "wordlists", "rockyou.txt.xz")

    if os.path.exists(rockyou_path):

        print("Performing initial setup ... ", end='', flush=True)

        rockyou_decomp_path = os.path.join(here, "static", "wordlists", "rockyou.txt")
        
        with lzma.open(rockyou_path) as rockyou:
            with open(rockyou_decomp_path, "wb") as f:
                f.write(rockyou.read())

        os.unlink(rockyou_path)

        print("[ DONE ]", flush=True)


##############
# Completers #
##############

class HashCrackCompleter(Completer):

    def get_completions(self, document, complete_event):
        
        # We done with first level?
        for word, func in MENU_FIRST_LEVEL.items():
            if document.text.split(" ")[0].lower() == word:
                return func["complete"](document, complete_event)
        
        for word in MENU_FIRST_LEVEL:
            if word.startswith(document.text.lower()):
                yield Completion(word, start_position=-len(word))

def complete_set(document, complete_event):
    pass

def complete_show(document, complete_event):
    pass

def complete_stub(document, complete_event):
    pass

#########
# doers #
#########

def do_set(inp):
    pass

def do_show(inpu):
    pass

def do_exit(*args):
    exit(0)

MENU_FIRST_LEVEL = {
        "set": {"complete": complete_set, "do": do_set},
        "show": {"complete": complete_show, "do": do_show},
        "exit": {"complete": complete_stub, "do": do_exit}
}

if __name__ == "__main__":
    main()
