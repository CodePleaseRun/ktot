import json
import time
from .manipulate import add_label
from .config import console_print, console, label_json, hotkeys_json


def load_hotkeys() -> dict:
    try:
        with open(hotkeys_json, 'r', encoding='UTF-8') as f:
            hotkey_dict = json.load(f)
    except FileNotFoundError:
        console_print(f'{hotkeys_json} not found', style='info')
        quit()
    return hotkey_dict


def load_labels() -> dict:
    labels = {}
    try:
        with console.status("Loading labels...", spinner="bouncingBall"):
            start_time = time.time()
            with open(label_json, "r", encoding='utf-8') as f:
                labels = json.load(f)
            time_taken = round(time.time() - start_time, 3)
        console_print(f'Labels loaded [{time_taken} secs]')
    except FileNotFoundError:
        console_print(
            f'[b cyan1]{label_json}[/] not found. Creating one.', style='info')
        open(label_json, "w", encoding='utf-8').close()
        add_label(labels)
    if len(labels) == 0:
        console_print(f'[b cyan1]{label_json}[/] is empty.', style='info')
        add_label(labels)
    return labels
