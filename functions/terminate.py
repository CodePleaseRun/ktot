from .config import console_print, console, key_at_index, label_json
from .toggle import toggle_timer
import time
import sys
import json


def clean_up(log, labels) -> None:
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        console_print(
            f'Deactivating [b cyan1]{label_name}[/] before quiting', style='info')
        toggle_timer(log, labels)
    with console.status("Saving labels...", spinner="bouncingBall"):
        start_time = time.time()
        with open(label_json, 'w', encoding='UTF-8') as f:
            json.dump(labels, f, indent=4)
        time_taken = round(time.time() - start_time, 3)
    console_print(f'Labels saved [{time_taken} secs]')
    console.rule('[b green_yellow]Tracker exited successfully[/]',
                 style='b bright_white')
    sys.exit()
