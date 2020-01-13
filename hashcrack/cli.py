
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import Completer, Completion

STYLE = Style.from_dict({
    # User input (default text).
    '':          '#89cb8c',

    # Prompt.
    'hashcat':  '#89a3cb',
    'whilte':   '#ffffff',
})

def main():
    
    prompt = [
            ('class:hashcat', 'hashcrack'),
            ('class:white', ' > ')
    ]

    session = PromptSession(prompt, style=STYLE, completer=HashCrackCompleter(), complete_while_typing=True)

    while True:

        try:
            out = session.prompt()
        except (KeyboardInterrupt, EOFError):
            return


def complete_set(document, complete_event):
    pass

def complete_show(document, complete_event):
    pass

class HashCrackCompleter(Completer):

    def get_completions(self, document, complete_event):
        
        # We done with first level?
        for word, func in FIRST_LEVEL.items():
            if document.text.split(" ")[0].lower() == word:
                return func(document, complete_event)
        
        for word in FIRST_LEVEL:
            if word.startswith(document.text.lower()):
                yield Completion(word, start_position=-len(word))

        #yield Completion('completion', start_position=0)

FIRST_LEVEL = {
        "set": complete_set,
        "show": complete_show,
}

if __name__ == "__main__":
    main()
