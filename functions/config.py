import sys
from rich.console import Console

console = Console()

label_json = 'json/labels.json'
hotkeys_json = 'json/hotkeys.json'

if sys.platform == 'linux':
    is_linux = True
else:
    is_linux = False


def key_at_index(list_name, index) -> str:
    return list(list_name.keys())[index]


def console_print(sentence, style='good') -> str:
    # overwriting unnecessary escape combos lik ^[^@, ^[^a, rich cannot print carriage return
    print('\r', end='')
    if style == 'ask':
        console.print(f'[b orchid1][?] {sentence}[/]')
    elif style == 'info':
        console.print(f'[b orange1][!] {sentence}[/]')
    else:
        console.print(f'[b green_yellow][+] {sentence}[/]')
