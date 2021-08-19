import datetime
from rich.padding import Padding
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from .config import console_print, console, key_at_index


def toggle_timer(log, labels) -> None:

    label_name = key_at_index(labels, log.cur_index)
    if log.active_label == False:
        log.start()
        log.active_label = True
        log_msg = f"[b green_yellow]Tracking for [b cyan1]'{label_name}'[/] initiated[/]"
        log_msg = Padding(log_msg, (1, 0))
        console.print(Padding(
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
        console.print(Padding(
            Panel.fit(message_group, style='deep_pink2', title='Tracker Update'), (1, 0)))


def toggle_label(log, labels, num) -> None:
    if log.active_label:
        label_name = key_at_index(labels, log.cur_index)
        console_print(
            f'[b cyan1]{label_name}[/] is currently active.', style='info')
        toggle_timer(log, labels)

    log.cur_index = (log.cur_index + num) % len(labels)
    label_name = key_at_index(labels, log.cur_index)
    console_print(
        f'Active label changed to [b cyan1]{label_name}[/]', style='info')
