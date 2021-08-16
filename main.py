from functions import function, intro
import click
import sys
from tracker import tracker
from rich.traceback import install
install(show_locals=True)  # fancy traceback


if sys.platform == 'win32':
    is_windows = True
    import keyboard
else:
    is_windows = False


@click.command()
@click.option('--banner', default=True, help='Show intro banner (default=True)')
@click.option('--timestamp', default=True, help='Save timestamp of each session (default=True)')
def main(banner, timestamp) -> None:
    log = tracker.Tracker(timestamp)
    hotkeys = function.load_hotkeys()
    intro.show_intro(hotkeys, banner)
    labels = function.load_labels()
    function.create_hotkeys(log, labels, hotkeys)
    if is_windows:
        exit_key = hotkeys['exit_tracker']['win']
        keyboard.wait(exit_key, suppress=True, trigger_on_release=True)
        function.clean_up(log, labels)


if __name__ == '__main__':
    main()
