import keyboard
import time
import datetime
import json
import sys
from rich import box
from rich.table import Table
from rich.padding import Padding
from rich.console import Console, Group
from rich.text import Text
from rich.panel import Panel
from rich import print as rprint
from rich.traceback import install


try:
    import termios  # flushes stdin buffer (filled with ASCII escape sequence)
    is_linux = True
except ImportError:
    is_linux = False

label_file_path = './labels.json'
key_at_index = lambda x, y: list(x.keys())[y]
print_success = lambda x: Padding(Text(f'\u2714  {x}', style='bold bright_green'), (0, 0, 1, 0))
console = Console()
install(show_locals=True)  # fancy taceback


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
        log_msg.append('Tracking for ', style='bright_green')
        log_msg.append(f"'{label_name}'", style='pale_turquoise1')
        log_msg.append(' initiated', style='bright_green')
        log_msg = Padding(log_msg, (1, 0))
        print('\r', end='')
        rprint(Padding(Panel.fit(log_msg, style='bright_green', title='Tracker Update'), (1, 0)))
    else:
        log.stop()
        log.active_label = False

        elapsed_time = log.stop_time - log.start_time
        latest_log = (log.start_time, log.stop_time, elapsed_time)
        labels[label_name].append(latest_log)

        log_msg = Text()
        log_msg.append('Tracking for ', style='bright_red')
        log_msg.append(f"'{label_name}'", style='pale_turquoise1')
        log_msg.append(' terminated', style='bright_red')
        elapsed_time = time.strftime('%H:%M:%S', time.gmtime(elapsed_time))
        session_len = Text(justify='center')
        session_len.append('Session lasted for ', style='bright_white')
        session_len.append(f'{elapsed_time}', style='dark_orange')
        message_group = Padding(Group(log_msg, session_len, fit=True), (1, 0))
        print('\r', end='')
        rprint(Padding(Panel.fit(message_group, style='bright_red', title='Tracker Update'), (1, 0)))


def load_labels() -> dict:
    labels = {}
    try:
        with console.status("Loading labels...", spinner="bouncingBall"):
            start_time = time.time()
            with open(label_file_path, "r", encoding='utf-8') as f:
                labels = json.load(f)
            time_taken = round(time.time() - start_time, 3)
        print('\r\t')  # first thing to get printed
        rprint(print_success(f'Labels loaded [{time_taken} secs]'))
    except FileNotFoundError:
        print(f'\r{label_file_path} not found. Creating one.')
        open(label_file_path, "w", encoding='utf-8').close()
        add_label(labels)
    if len(labels) == 0:
        print(f'\r{label_file_path} contains no label.')
        add_label(labels)
    return labels


def show_labels(log, labels) -> None:

    table = Table(box=box.ROUNDED)
    table.add_column(Text("Label Name", style='white'), justify="center", style="bold green3")

    column_add = lambda x: table.add_column(Text(x), justify="center", style="bold dark_orange")
    column_add('Total Sessions')
    column_add('Total Session Time')
    column_add('Longest Session Time')
    column_add('Average Session Time')
    column_add('Latest Session Time')

    for key, value in labels.items():

        name = Padding(key, (0, 0, 1, 0), expand=False)
        sessions = len(value)
        if sessions == 0:
            total_time = av_time = last_time = longes_time = '00:00:00'
        else:
            elapsed_time = [i[2] for i in value]
            get_time_str = lambda x: str(datetime.timedelta(seconds=round(x)))
            total_time = get_time_str(sum(elapsed_time))
            longes_time = get_time_str(max(elapsed_time))
            av_time = get_time_str(sum(elapsed_time) / sessions)
            last_time = get_time_str(value[-1][2])

        table.add_row(name, str(sessions), total_time, longes_time, av_time, last_time)
    label_name = key_at_index(labels, log.cur_index)
    s1 = Text.assemble(('Currently selected: ', 'bright_white'), (f"'{label_name}'", 'bold green3'))
    s2 = Text.assemble(('Is active: ', 'bright_white'), (f'{log.active_label}', 'italic bold bright_red'))
    table_group = Group(table, s1, s2)  # (s2, fit=True)
    print('\r', end='')
    rprint(Padding(Panel.fit(table_group, title='Label Statistics', style='bright_white'), (0, 0, 1, 0)))


def add_label(labels) -> None:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    new_label = input('\rEnter the new label: ').strip()
    if new_label in labels.keys():
        print(f'\r{new_label} already exist as a label.')
    else:
        labels[new_label] = []
        print(f'\rAdded label: {new_label}')


def toggle_label(log, labels, num) -> None:
    if log.active_label:
        print('\rA label was already active. Stopping it.')
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + num) % len(labels)
    print(f'\rActive label changed to {key_at_index(labels,log.cur_index)}')


def create_hotkeys(log, labels) -> None:
    keyboard.add_hotkey('ctrl+alt+space', lambda: toggle_timer(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+n', lambda: toggle_label(log, labels, 1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+p', lambda: toggle_label(log, labels, -1),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+l', lambda: show_labels(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+a', lambda: add_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+u', lambda: update_label(labels),
                        suppress=True, trigger_on_release=True)
    print('\r', end='')
    rprint(print_success('Hotkeys Created'))


def clean_up(log, labels) -> None:
    keyboard.unhook_all()
    if log.active_label:
        print('\rDeactivating the label.')
        toggle_timer(log, labels)
    with console.status("Saving labels...", spinner="bouncingBall"):
        start_time = time.time()
        with open(label_file_path, 'w', encoding='UTF-8') as f:
            json.dump(labels, f, indent=4)
        time_taken = round(time.time() - start_time, 3)
    print('\r', end='')
    rprint(print_success(f'Labels Saved [{time_taken} secs]'))
    console.rule('[b bright_green]Tracker exited successfully[/]')


def update_label(labels) -> None:
    old_label = input('\rEnter old label: ').strip()
    if old_label in labels.keys():
        new_label = input('\rEnter new label: ').strip()
        if new_label in labels.keys():
            print(f'\rLable "{new_label}" already exist.')
        else:
            labels[new_label] = labels.pop(old_label)
            print(f'\r"{old_label}" updated to "{new_label}".')
    else:
        print(f'\r"{old_label}" is not a label.')
    return 0


def main() -> None:
    labels = load_labels()
    log = Tracker()
    create_hotkeys(log, labels)
    keyboard.wait('ctrl+alt+e', suppress=True, trigger_on_release=True)
    clean_up(log, labels)


if __name__ == '__main__':
    main()
