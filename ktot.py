from functions.intro import show_intro
import click
from tracker import tracker
from functions.load import load_labels, load_hotkeys
from functions.create_hotkeys import create_hotkeys
from functions.terminate import clean_up
from functions.config import is_linux
from rich.traceback import install
install(show_locals=True)  # fancy traceback


if not is_linux:
    import keyboard


@click.command()
@click.option('--banner', default=True, help='Show intro banner (default=True)')
@click.option('--timestamp', default=True, help='Save timestamp of each session (default=True)')
def main(banner, timestamp) -> None:
    log = tracker.Tracker(timestamp)
    hotkeys = load_hotkeys()
    show_intro(hotkeys, banner)
    labels = load_labels()
    create_hotkeys(log, labels, hotkeys)
    if not is_linux:
        exit_key = hotkeys['exit_tracker']['win']
        keyboard.wait(exit_key, suppress=True, trigger_on_release=True)
        clean_up(log, labels)


if __name__ == '__main__':
    main()
