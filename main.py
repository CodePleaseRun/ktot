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


class Logger:

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
        print(
            hp.info(hp.yellow(f'\rLog started for {label_name}')))
        # print(
        #    hp.info(hp.yellow(f'\rLog started for {labels[log.cur_index]}')))
    else:
        log.stop()
        log.active_label = False

        elapsed_time = log.stop_time - log.start_time
        latest_log = (log.start_time, log.stop_time, elapsed_time)
        labels[label_name].append(latest_log)

        print(f'\rLog ended for {label_name}')
        #print(f'\rLog ended for {labels[log.cur_index]}')

        print(f"\r{hp.info((hp.yellow(f'{elapsed_time=}')))}")


def load_labels() -> dict:
    try:
        with open(label_file_path, "r", encoding='utf-8') as f:
            labels = json.load(f)
            print('\rLabels loaded successfully')
        if len(labels) == 0:
            print('\rThere are no labels.')
            add_label(labels)
            # quit()

    except Exception as e:
        print(str(e))
        quit()
    return labels


def add_label(labels) -> None:
    #! https://abelbeck.wordpress.com/2013/08/29/clear-sys-stdin-buffer/
    if is_linux:
        termios.tcflush(sys.stdin, termios.TCIFLUSH)
    new_label = input('\rEnter the new label: ')
    new_label.strip()
    labels[new_label] = []  # .append(new_label.strip())
    # labels.sort()
    with open(label_file_path, 'w', encoding='UTF-8') as f:
        json.dump(labels, f, indent=4)
    print(f'\rAdded label: {new_label}')


def toggle_label(log, labels) -> None:
    if log.active_label:
        print('\rA label was already active. Stopping it.')
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + 1) % len(labels)
    #print(f'\rCurrent active label changed to {labels[log.cur_index]}')
    print(
        f'\rCurrent active label changed to {key_at_index(labels,log.cur_index)}')


def create_hotkeys(log, labels) -> None:
    keyboard.add_hotkey('ctrl+alt+space', lambda: toggle_timer(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+n', lambda: toggle_label(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey('ctrl+alt+a', lambda: add_label(labels),
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


def main() -> None:
    labels = load_labels()
    log = Logger()
    create_hotkeys(log, labels)
    print('Created Hotkeys')
    keyboard.wait('ctrl+alt+e', suppress=True, trigger_on_release=True)
    clean_up(log, labels)


if __name__ == '__main__':
    main()
