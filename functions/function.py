import sys
import time
import json
import datetime
from rich import box
from typing import Union
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.padding import Padding
from rich.console import Console, Group
from rich.prompt import Prompt, Confirm

if sys.platform == 'linux':
    is_linux = True
    import termios  # only in Linux, for flushing stdin
    from pynput import keyboard
else:
    is_linux = False
    import keyboard


label_file_path = 'json/labels.json'
hotkeys_file_path = 'json/hotkeys.json'
key_at_index = lambda x, y: list(x.keys())[y]
print_good = lambda x: f'[b green_yellow][+] {x}[/]'
print_info = lambda x: f'[b orange1][!] {x}[/]'
print_ask = lambda x: f'[b orchid1][?] {x}[/]'


console = Console()


def console_print(sentence):
    print('\r', end='')  # overwriting unnecessary escape combos lik ^[^@, ^[^a
    console.print(sentence)  # rich cannot print carriage return


def load_hotkeys() -> dict:
    try:
        with open(hotkeys_file_path, 'r', encoding='UTF-8') as f:
            hotkey_dict = json.load(f)
    except FileNotFoundError:
        console_print(print_info(f'{hotkeys_file_path} not found'))
        quit()
    return hotkey_dict


def load_labels() -> dict:
    labels = {}
    try:
        with console.status("Loading labels...", spinner="bouncingBall"):
            start_time = time.time()
            with open(label_file_path, "r", encoding='utf-8') as f:
                labels = json.load(f)
            time_taken = round(time.time() - start_time, 3)
        console_print(print_good(f'Labels loaded [{time_taken} secs]'))
    except FileNotFoundError:
        console_print(print_info(
            f'[b cyan1]{label_file_path}[/] not found. Creating one.'))
        open(label_file_path, "w", encoding='utf-8').close()
        add_label(labels)
    if len(labels) == 0:
        console_print(print_info(f'[b cyan]{label_file_path}[/] is empty.'))
        add_label(labels)
    return labels


def create_hotkeys_win(log, labels, hotkeys) -> None:
    toggle = hotkeys['toggle']["win"]
    next_label = hotkeys['next_label']["win"]
    prev_label = hotkeys['prev_label']["win"]
    label_add = hotkeys['label_add']["win"]
    label_del = hotkeys['label_del']["win"]
    label_update = hotkeys['label_update']["win"]
    label_stats = hotkeys['label_stats']["win"]
    show_hotkeys = hotkeys['show_hotkeys']["win"]
    keyboard.add_hotkey(toggle, lambda: toggle_timer(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(next_label, lambda: toggle_label(log, labels, 1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(prev_label, lambda: toggle_label(log, labels, -1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_add, lambda: add_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_del, lambda: delete_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_update, lambda: update_label(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_stats, lambda: show_labels(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(show_hotkeys, lambda: show_controls(hotkeys),
                        suppress=True, trigger_on_release=True)
    console_print(print_good('Hotkeys Created'))
    console.rule('[b green_yellow]Ready to use[/]', style='b bright_white')


def create_hotkeys_linux(log, labels, hotkeys) -> None:
    toggle = hotkeys['toggle']["linux"]
    next_label = hotkeys['next_label']["linux"]
    prev_label = hotkeys['prev_label']["linux"]
    label_add = hotkeys['label_add']["linux"]
    label_del = hotkeys['label_del']["linux"]
    label_update = hotkeys['label_update']["linux"]
    label_stats = hotkeys['label_stats']["linux"]
    show_hotkeys = hotkeys['show_hotkeys']["linux"]
    tracker_exit = hotkeys['exit_tracker']["linux"]
    with keyboard.GlobalHotKeys({
            toggle: lambda: toggle_timer(log, labels),
            next_label: lambda: toggle_label(log, labels, 1),
            prev_label: lambda: toggle_label(log, labels, -1),
            label_add: lambda: add_label(labels),
            label_del: lambda: delete_label(labels),
            label_update: lambda: update_label(log, labels),
            label_stats: lambda: show_labels(log, labels),
            tracker_exit: lambda: clean_up(log, labels),
            show_hotkeys: lambda: show_controls(hotkeys)}) as h:
        console_print(print_good('Hotkeys Created'))
        console.rule('[b green_yellow]Ready to use[/]', style='b bright_white')
        h.join()


if is_linux:
    create_hotkeys = create_hotkeys_linux
else:
    create_hotkeys = create_hotkeys_win


def toggle_timer(log, labels) -> None:

    label_name = key_at_index(labels, log.cur_index)
    if log.active_label == False:
        log.start()
        log.active_label = True
        log_msg = f"[b green_yellow]Tracking for [b cyan1]'{label_name}'[/] initiated[/]"
        log_msg = Padding(log_msg, (1, 0))
        console_print(Padding(
            Panel.fit(log_msg, style='green_yellow', title='Tracker Update'), (1, 0)))
    else:
        log.stop()
        log.active_label = False
        elapsed_time = log.stop_time - log.start_time
        latest_log = [log.start_time, log.stop_time, elapsed_time]
        if log.timestamp == False:
            latest_log[0] = latest_log[1] = -1
        labels[label_name].append(latest_log)
        log_msg = f"[b deep_pink2]Tracking for [b cyan1]'{label_name}'[/] terminated[/]"
        elapsed_time = str(datetime.timedelta(seconds=round(elapsed_time)))
        session_len = Text(justify='center')
        session_len.append('Session lasted for ', style='b bright_white')
        session_len.append(f'{elapsed_time}', style='b orange1')
        message_group = Padding(Group(log_msg, session_len, fit=True), (1, 0))
        console_print(Padding(
            Panel.fit(message_group, style='deep_pink2', title='Tracker Update'), (1, 0)))


def toggle_label(log, labels, num) -> None:
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        console_print(print_info(
            f'[b cyan1]{label_name}[/] is currently active.'))
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + num) % len(labels)
    label_name = key_at_index(labels, log.cur_index)
    console_print(print_info(
        f'Active label changed to [b cyan1]{label_name}[/]'))


def add_label(labels) -> Union[str, bool]:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    is_added = False
    print('\r', end='')
    new_label = Prompt.ask(print_ask('Enter the new label')).strip()
    if new_label in labels.keys():
        console_print(print_info(f'[b cyan1]{new_label}[/] already exist'))
    else:
        labels[new_label] = []
        console_print(print_good(f'[b cyan1]{new_label}[/] added'))
        is_added = True
    return(new_label, is_added)


def delete_label(labels) -> None:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    is_added = False
    print('\r', end='')
    del_label = Prompt.ask(print_ask('Label to be deleted')).strip()
    if del_label in labels.keys():
        print('\r', end='')
        final_ask = Confirm.ask(print_ask('Are you sure?'))
        if final_ask == True:
            labels.pop(del_label)
            console_print(print_info(f'[b cyan1]{del_label}[/] deleted'))
        else:
            console_print(print_good(f'[b cyan1]{del_label}[/] stays!'))
    else:
        console_print(print_info(f'[b cyan1]{del_label}[/] is not a label'))


def update_label(log, labels) -> None:
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    print('\r', end='')
    old_label = Prompt.ask(print_ask('Label to be updated')).strip()
    if old_label in labels.keys():
        new_label, is_added = add_label(labels)
        if is_added:
            if log.active_label:
                console_print(print_info(
                    f'Deactivating [b cyan1]{old_label}[/] before updating'))
                toggle_timer(log, labels)

            labels[new_label] = labels.pop(old_label)
            console_print(print_good(
                f'[b cyan1]{old_label}[/] updated to [b cyan1]{new_label}[/]'))
    else:
        console_print(print_info(f'[b cyan1]{old_label}[/] is not a label'))


def show_labels(log, labels) -> None:

    table = Table(box=box.ROUNDED)
    table.add_column("Label Name", justify="center",
                     style="b green_yellow", no_wrap=True)

    column_add = lambda x: table.add_column(
        Text(x), justify="center", style="b orange1")
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
            elapsed_time = [i[-1] for i in value]
            get_time_str = lambda x: str(datetime.timedelta(seconds=round(x)))
            total_time = get_time_str(sum(elapsed_time))
            longes_time = get_time_str(max(elapsed_time))
            av_time = get_time_str(sum(elapsed_time) / sessions)
            last_time = get_time_str(value[-1][2])
        table.add_row(name, str(sessions), total_time,
                      longes_time, av_time, last_time)

    label_name = key_at_index(labels, log.cur_index)
    s1 = Text.assemble(('Currently selected: ', 'bright_white'),
                       (f'{label_name}', 'b green_yellow'))
    s2 = Text.assemble(('Is active: ', 'bright_white'),
                       (f'{log.active_label}', 'italic b deep_pink2'))
    table_group = Group(table, s1, s2)  # (s2, fit=True)
    outer_panel = Panel.fit(
        table_group, title='Label Statistics', style='bright_white')
    console_print(Padding(outer_panel, (1, 0)))


def show_controls(hotkeys) -> None:
    table = Table(box=box.ROUNDED, title='Control Scheme',
                  style='b bright_white')
    table.add_column('Hotkey', justify="center", style="b green_yellow")
    table.add_column('Description', justify="center", style="b orange1")
    for value in hotkeys.values():
        hk_name = value['win'].replace('+', ' + ').title() + '\n'
        hk_desc = value['desc']
        table.add_row(hk_name, hk_desc)
    console_print(Padding(table, (1, 0)))


def clean_up(log, labels) -> None:
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        console_print(print_info(
            f'Deactivating [b cyan1]{label_name}[/] before quiting'))
        toggle_timer(log, labels)
    with console.status("Saving labels...", spinner="bouncingBall"):
        start_time = time.time()
        with open(label_file_path, 'w', encoding='UTF-8') as f:
            json.dump(labels, f, indent=4)
        time_taken = round(time.time() - start_time, 3)
    console_print(print_good(f'Labels saved [{time_taken} secs]'))
    console.rule('[b green_yellow]Tracker exited successfully[/]',
                 style='b bright_white')
    sys.exit()
