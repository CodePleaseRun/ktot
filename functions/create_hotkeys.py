from .config import console_print, console, is_linux
from .toggle import toggle_timer, toggle_label
from .manipulate import add_label, delete_label, update_label
from .show import show_labels, show_controls
from .terminate import clean_up

if is_linux:
    from pynput import keyboard
else:
    import keyboard


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
    keyboard.add_hotkey(label_del, lambda: delete_label(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_update, lambda: update_label(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(label_stats, lambda: show_labels(log, labels),
                        suppress=True, trigger_on_release=True)
    keyboard.add_hotkey(show_hotkeys, lambda: show_controls(hotkeys),
                        suppress=True, trigger_on_release=True)
    console_print('Hotkeys Created')
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
            label_del: lambda: delete_label(log, labels),
            label_update: lambda: update_label(log, labels),
            label_stats: lambda: show_labels(log, labels),
            tracker_exit: lambda: clean_up(log, labels),
            show_hotkeys: lambda: show_controls(hotkeys)}) as h:
        console_print('Hotkeys Created')
        console.rule('[b green_yellow]Ready to use[/]', style='b bright_white')
        h.join()


if is_linux:
    create_hotkeys = create_hotkeys_linux
else:
    create_hotkeys = create_hotkeys_win
