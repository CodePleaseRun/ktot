from typing import Union
from rich.prompt import Prompt, Confirm
from .config import console_print, is_linux, label_json
from .toggle import toggle_timer, toggle_label

if is_linux:
    import sys
    import termios


def add_label(labels) -> Union[str, bool]:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    is_added = False
    print('\r', end='')
    new_label = Prompt.ask('[b orchid1][?] New label name[/]').strip()
    if new_label in labels.keys():
        console_print(f'[b cyan1]{new_label}[/] already exist', style='info')
    else:
        labels[new_label] = []
        console_print(f'[b cyan1]{new_label}[/] added')
        is_added = True
    return(new_label, is_added)


def delete_label(log, labels) -> None:
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    print('\r', end='')
    del_label = Prompt.ask('[b orchid1][?] Label to be deleted[/]').strip()
    if del_label in labels.keys():
        print('\r', end='')
        final_ask = Confirm.ask('[b orchid1][?] Are you sure?[/]')
        if final_ask == True:
            if log.active_label:
                console_print(
                    f'Deactivating [b cyan1]{del_label}[/] before deleting', style='info')
                toggle_timer(log, labels)
            labels.pop(del_label)
            console_print(f'[b cyan1]{del_label}[/] deleted', style='info')
            if len(labels) == 0:
                console_print(
                    f'[b cyan1]{label_json}[/] is empty.', style='info')
                add_label(labels)
            else:
                toggle_label(log, labels, 0)
        else:
            console_print(f'[b cyan1]{del_label}[/] stays!')
    else:
        console_print(f'[b cyan1]{del_label}[/] is not a label', style='info')


def update_label(log, labels) -> None:
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    print('\r', end='')
    old_label = Prompt.ask('[b orchid1][?] Label to be updated[/]').strip()
    if old_label in labels.keys():
        new_label, is_added = add_label(labels)
        if is_added:
            if log.active_label:
                console_print(
                    f'Deactivating [b cyan1]{old_label}[/] before updating', style='info')
                toggle_timer(log, labels)

            labels[new_label] = labels.pop(old_label)
            console_print(
                f'[b cyan1]{old_label}[/] updated to [b cyan1]{new_label}[/]')
    else:
        console_print(f'[b cyan1]{old_label}[/] is not a label', style='info')
