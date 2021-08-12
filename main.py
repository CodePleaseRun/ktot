import keyboard
import time
import json
import sys
import huepy as hp

try:
    import termios  # flushes stdin buffer (filled with ASCII escape sequence)
    is_linux = True
except ImportError:
    is_linux = False

label_file_path = './labels.json'
key_at_index = lambda x, y: list(x.keys())[y]


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
        print(hp.info(hp.yellow(f'\rLog started for {label_name}')))
    else:
        log.stop()
        log.active_label = False

        elapsed_time = log.stop_time - log.start_time
        latest_log = (log.start_time, log.stop_time, elapsed_time)
        labels[label_name].append(latest_log)

        print(f'\rLog ended for {label_name}')
        print(f"\r{hp.info((hp.yellow(f'{elapsed_time=}')))}")


def load_labels() -> dict:
    labels = {}
    try:
        with open(label_file_path, "r", encoding='utf-8') as f:
            labels = json.load(f)
            print('\rLabels loaded successfully')
        if len(labels) == 0:
            print(f'\r{label_file_path} contains no label.')
            add_label(labels)

    except FileNotFoundError:
        print(f'\r{label_file_path} not found. Creating one.')
        open(label_file_path, "w", encoding='utf-8').close()
        add_label(labels)
    return labels


def show_labels(log, labels) -> None:
    print('\rList of all labels:')
    for key, value in labels.items():
        print(f"\r{key}, total sessions = {len(value)}")
    print(f'\rCurrently selected label: {key_at_index(labels, log.cur_index)}')
    print(f'\rIs active: {log.active_label}')


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


def toggle_label(log, labels) -> None:
    if log.active_label:
        print('\rA label was already active. Stopping it.')
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + 1) % len(labels)
    print(f'\rActive label changed to {key_at_index(labels,log.cur_index)}')


def create_hotkeys(log, labels) -> None:
    keyboard.add_hotkey('ctrl+alt+space', lambda: toggle_timer(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+n', lambda: toggle_label(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+l', lambda: show_labels(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+a', lambda: add_label(labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+u', lambda: update_label(labels),
                        suppress=True, trigger_on_release=True)


def clean_up(log, labels) -> None:
    keyboard.unhook_all()
    if log.active_label:
        print('\rDeactivating the label.')
        toggle_timer(log, labels)
    print(f'\rTracker Deactivated.\nSaving log.')
    with open(label_file_path, 'w', encoding='UTF-8') as f:
        json.dump(labels, f, indent=4)
    print('\rLog Saved.')


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
    print('\rCreated Hotkeys')
    keyboard.wait('ctrl+alt+e', suppress=True, trigger_on_release=True)
    clean_up(log, labels)


if __name__ == '__main__':
    main()
