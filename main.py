import keyboard
import time
import datetime
import json
import sys
from typing import Union
from rich import box
from rich.table import Table
from rich.padding import Padding
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich.traceback import install
from rich.prompt import Prompt


try:
    import termios  # flushes stdin buffer (filled with ASCII escape sequence)
    is_linux = True
except ImportError:
    is_linux = False
label_file_path = './labels.json'
hotkeys_file_path = './hotkeys.json'
key_at_index = lambda x, y: list(x.keys())[y]
print_good = lambda x: f'[b green_yellow][+] {x}[/]'
print_info = lambda x: f'[b orange1][!] {x}[/]'
print_ask = lambda x: f'[b orchid1][?] {x}[/]'
console = Console()
install(show_locals=True)  # fancy traceback


class Tracker:

    def __init__(self, cur_index=0) -> None:
        self.active_label = False
        self.cur_index = cur_index
        self.start_time = 0
        self.stop_time = 0

    def start(self) -> float:
        self.start_time = time.time()
        return self.start_time

    def stop(self) -> float:
        self.stop_time = time.time()
        return self.stop_time


def toggle_timer(log, labels) -> None:

    label_name = key_at_index(labels, log.cur_index)
    if log.active_label == False:
        log.start()
        log.active_label = True
        log_msg = Text()
        log_msg.append('Tracking for ', style=' b green_yellow')
        log_msg.append(f"'{label_name}'", style='b cyan1')
        log_msg.append(' initiated', style='b green_yellow')
        log_msg = Padding(log_msg, (1, 0))
        print('\r', end='')
        console.print(Padding(Panel.fit(log_msg, style='green_yellow', title='Tracker Update'), (1, 0)))
    else:
        log.stop()
        log.active_label = False
        elapsed_time = log.stop_time - log.start_time
        latest_log = (log.start_time, log.stop_time, elapsed_time)
        labels[label_name].append(latest_log)
        log_msg = Text()
        log_msg.append('Tracking for ', style='b deep_pink2')
        log_msg.append(f"'{label_name}'", style='b cyan1')
        log_msg.append(' terminated', style='b deep_pink2')
        elapsed_time = str(datetime.timedelta(seconds=round(elapsed_time)))
        session_len = Text(justify='center')
        session_len.append('Session lasted for ', style='b bright_white')
        session_len.append(f'{elapsed_time}', style='b orange1')
        message_group = Padding(Group(log_msg, session_len, fit=True), (1, 0))
        print('\r', end='')
        console.print(Padding(Panel.fit(message_group, style='deep_pink2', title='Tracker Update'), (1, 0)))


def load_labels() -> dict:
    labels = {}
    try:
        with console.status("Loading labels...", spinner="bouncingBall"):
            start_time = time.time()
            with open(label_file_path, "r", encoding='utf-8') as f:
                labels = json.load(f)
            time_taken = round(time.time() - start_time, 3)
        console.print(print_good(f'Labels loaded [{time_taken} secs]'))
    except FileNotFoundError:
        print('\r', end='')
        console.print(print_info(f'[b cyan1]{label_file_path}[/] not found. Creating one.'))
        open(label_file_path, "w", encoding='utf-8').close()
        add_label(labels)
    if len(labels) == 0:
        print('\r', end='')
        console.print(print_info(f'[b cyan]{label_file_path}[/] is empty.'))
        add_label(labels)
    return labels


def show_labels(log, labels) -> None:

    table = Table(box=box.ROUNDED)
    table.add_column("Label Name", justify="center", style="b green_yellow")
    column_add = lambda x: table.add_column(Text(x), justify="center", style="b orange1")
    column_add('Total Sessions')
    column_add('Total Session Time')
    column_add('Longest Session Time')
    column_add('Average Session Time')
    column_add('Latest Session Time')

    for key, value in labels.items():
        name = f'{key}\n'
        sessions = len(value)
        if sessions == 0:
            total_time = av_time = last_time = longes_time = '0:00:00'
        else:
            elapsed_time = [i[2] for i in value]
            get_time_str = lambda x: str(datetime.timedelta(seconds=round(x)))
            total_time = get_time_str(sum(elapsed_time))
            longes_time = get_time_str(max(elapsed_time))
            av_time = get_time_str(sum(elapsed_time) / sessions)
            last_time = get_time_str(value[-1][2])
        table.add_row(name, str(sessions), total_time, longes_time, av_time, last_time)

    label_name = key_at_index(labels, log.cur_index)
    s1 = Text.assemble(('Currently selected: ', 'bright_white'), (f'{label_name}', 'b green_yellow'))
    s2 = Text.assemble(('Is active: ', 'bright_white'), (f'{log.active_label}', 'italic b deep_pink2'))
    table_group = Group(table, s1, s2)  # (s2, fit=True)
    print('\r', end='')
    outer_panel = Panel.fit(table_group, title='Label Statistics', style='bright_white')
    console.print(Padding(outer_panel, (1, 0)))


def add_label(labels) -> Union[str, bool]:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    is_added = False
    print('\r', end='')
    new_label = Prompt.ask(print_ask('Enter the new label: ')).strip()
    if new_label in labels.keys():
        print('\r', end='')
        console.print(print_info(f'[b cyan1]{new_label}[/] already exist'))
    else:
        labels[new_label] = []
        print('\r', end='')
        console.print(print_good(f'[b cyan1]{new_label}[/] added'))
        is_added = True
    return(new_label, is_added)


def toggle_label(log, labels, num) -> None:
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        print('\r', end='')
        console.print(print_info(f'[b cyan1]{label_name}[/] is currently active.'))
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + num) % len(labels)
    label_name = key_at_index(labels, log.cur_index)
    print('\r', end='')
    console.print(print_info(f'Active label changed to [b cyan1]{label_name}[/]'))


def create_hotkeys(log, labels, hotkeys) -> None:
    toggle = hotkeys['toggle'][0]
    next_label = hotkeys['next_label'][0]
    prev_label = hotkeys['prev_label'][0]
    label_add = hotkeys['label_add'][0]
    label_update = hotkeys['label_update'][0]
    label_stats = hotkeys['label_stats'][0]
    show_hotkeys = hotkeys['show_hotkeys'][0]
    keyboard.add_hotkey(toggle, lambda: toggle_timer(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(next_label, lambda: toggle_label(log, labels, 1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(prev_label, lambda: toggle_label(log, labels, -1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_add, lambda: add_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_update, lambda: update_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_stats, lambda: show_labels(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(show_hotkeys, lambda: show_controls(hotkeys),
                        suppress=True, trigger_on_release=True)
    print('\r', end='')
    console.print(print_good('Hotkeys Created'))


def show_controls(hotkeys) -> None:
    table = Table(box=box.ROUNDED, title='Control Scheme', style='b bright_white')
    table.add_column('Hotkeys', justify="center", style="b green_yellow")
    table.add_column('Description', justify="center", style="b orange1")
    for value in hotkeys.values():
        hk_name = value[0].replace('+', ' + ').title() + '\n'
        hk_desc = value[1]
        table.add_row(hk_name, hk_desc)
    print('\r', end='')
    console.print(Padding(table, (1, 0)))


def load_hotkeys() -> dict:
    try:
        with open(hotkeys_file_path, 'r', encoding='UTF-8') as f:
            hotkey_dict = json.load(f)
    except FileNotFoundError:
        console.print(print_info(f'{hotkeys_file_path} not found'))
        quit()
    return hotkey_dict


def clean_up(log, labels) -> None:
    keyboard.unhook_all()
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        print('\r', end='')
        console.print(print_info(f'Deactivating [b cyan1]{label_name}[/] before quiting'))
        toggle_timer(log, labels)
    with console.status("Saving labels...", spinner="bouncingBall"):
        start_time = time.time()
        with open(label_file_path, 'w', encoding='UTF-8') as f:
            json.dump(labels, f, indent=4)
        time_taken = round(time.time() - start_time, 3)
    print('\r', end='')
    console.print(print_good(f'Labels Saved [{time_taken} secs]'))
    console.rule('[b green_yellow]Tracker exited successfully[/]')


def update_label(labels) -> None:
    print('\r', end='')
    old_label = Prompt.ask(print_ask('Label to be updated: ')).strip()
    if old_label in labels.keys():
        new_label, is_added = add_label(labels)
        if is_added:
            labels[new_label] = labels.pop(old_label)
            print('\r', end='')
            console.print(print_good(f'[b cyan1]{old_label}[/] updated to [b cyan1]{new_label}[/]'))
    else:
        print('\r', end='')
        console.print(print_info(f'[b cyan1]{old_label}[/] is not a label'))


def main() -> None:
    labels = load_labels()
    hotkeys = load_hotkeys()
    log = Tracker()
    create_hotkeys(log, labels, hotkeys)
    exit_key = hotkeys['exit_tracker'][0]
    keyboard.wait(exit_key, suppress=True, trigger_on_release=True)
    clean_up(log, labels)


if __name__ == '__main__':
    main()
