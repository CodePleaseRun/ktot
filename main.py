import function
import sys
from tracker import Tracker
from rich.traceback import install
from intro import show_intro
install(show_locals=True)  # fancy traceback


if sys.platform == 'win32':
    is_windows = True
    import keyboard
else:
    is_windows = False


def main() -> None:
    log = Tracker()
    hotkeys = function.load_hotkeys()
    show_intro(hotkeys)
    labels = function.load_labels()
    function.create_hotkeys(log, labels, hotkeys)
    if is_windows:
        exit_key = hotkeys['exit_tracker']['win']
        keyboard.wait(exit_key, suppress=True, trigger_on_release=True)
        function.clean_up(log, labels)


if __name__ == '__main__':
    main()
