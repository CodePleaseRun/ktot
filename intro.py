from rich.text import Text
from rich.panel import Panel
from rich.padding import Padding
from rich.console import Console, Group

title1 = '''
  ██╗  ██╗███████╗███████╗██████╗      █████╗     ████████╗██████╗  █████╗  ██████╗██╗  ██╗
  ██║ ██╔╝██╔════╝██╔════╝██╔══██╗    ██╔══██╗    ╚══██╔══╝██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
  █████╔╝ █████╗  █████╗  ██████╔╝    ███████║       ██║   ██████╔╝███████║██║     █████╔╝
  ██╔═██╗ ██╔══╝  ██╔══╝  ██╔═══╝     ██╔══██║       ██║   ██╔══██╗██╔══██║██║     ██╔═██╗
  ██║  ██╗███████╗███████╗██║         ██║  ██║       ██║   ██║  ██║██║  ██║╚██████╗██║  ██╗
  ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝         ╚═╝  ╚═╝       ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
  '''

console = Console()


def show_intro(hotkeys, show=True) -> None:

    if show:
        help_key = hotkeys['show_hotkeys']['win']
        help_key = help_key.replace('+', ' + ').title().replace(' + ', '+')
        help_text = f'{help_key}: Show controls'
        desc = Text(f'A SIMPLE, HOTKEYS-BASED TIME TRACKER\n\n',
                    justify='center', style='b orange1')
        desc.append(help_text, style='b cyan1')
        desc_panel = Panel(desc, border_style='b deep_pink2')
        title_panel = Panel.fit(Text(title1, style='b green_yellow'),
                                border_style='b')
        intro_group = Panel.fit(Group(title_panel, desc_panel),
                                border_style='b')
        console.print(Padding(intro_group, (1, 0)))
    else:
        pass
