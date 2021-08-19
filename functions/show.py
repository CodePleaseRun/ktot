from rich.table import Table
from rich.text import Text
from rich import box
import datetime
from rich.console import Group
from rich.panel import Panel
from rich.padding import Padding
from .config import console_print, console, label_json, key_at_index


def show_labels(log, labels) -> None:

    if len(labels) == 0:
        console_print(f'[b cyan1]{label_json}[/] is empty.', style='info')
        return
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
    console.print(Padding(outer_panel, (1, 0)))


def show_controls(hotkeys) -> None:
    table = Table(box=box.ROUNDED, title='Control Scheme',
                  style='b bright_white')
    table.add_column('Hotkey', justify="center", style="b green_yellow")
    table.add_column('Description', justify="center", style="b orange1")
    for value in hotkeys.values():
        hk_name = value['win'].replace('+', ' + ').title() + '\n'
        hk_desc = value['desc']
        table.add_row(hk_name, hk_desc)
    console.print(Padding(table, (1, 0)))
