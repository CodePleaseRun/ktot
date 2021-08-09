from pynput import keyboard
import time
import json


class Logger:

    def __init__(self, cur_label_index=0):
        self.active_label = False
        self.cur_label_index = cur_label_index
        self.start_time = 0

    def start(self):
        self.start_time = time.time()

    def stop(self):
        elapsed_time = time.time() - self.start_time
        return elapsed_time


def toggle_timer(log, labels):

    if log.active_label == False:
        log.start()
        log.active_label = True
        print(f'Log started for {labels[log.cur_label_index]}')
    else:
        elapsed_time = log.stop()
        log.active_label = False
        print(f'Log ended for {labels[log.cur_label_index]}')
        print(f'{elapsed_time=}')


def load_labels():
    try:
        with open("labels.json", "r", encoding='utf-8') as f:
            labels = json.load(f)['labels']
            print('Labels loaded successfully')
        if len(labels) == 0:
            print('Labels list if empty')
            quit()

    except:
        print('file labels.json not found')
        quit()
    return labels


def toggle_label(log, labels):
    if log.active_label:
        print('A label was already active. Stopping it.')
        toggle_timer(log, labels)

    log.cur_label_index = (log.cur_label_index + 1) % len(labels)
    print(f'Current active label changed to {labels[log.cur_label_index]}')
    toggle_timer(log, labels)


def main():
    labels = load_labels()
    log = Logger()

    def run_toggle_timer():
        toggle_timer(log, labels)

    def run_toggle_label():
        toggle_label(log, labels)

    with keyboard.GlobalHotKeys({
            '<shift>+<space>': run_toggle_timer,
            '<shift>+<right>': run_toggle_label,
            '<esc>': exit, }) as h:
        h.join()


if __name__ == '__main__':
    main()
