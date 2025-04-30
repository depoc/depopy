import click
import sys
import itertools
import time
import math

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from typing import Literal

from depoc.objects.base import DepocObject

console = Console()

emojis = {
    'ID': ':white_medium_star:',
    'Name': '✏️ ',
    'Email': '✉️ ',
    'Phone': '📱',
    'Username': '👤',
    'Active': '🟢',
    'Staff': '💼',
    'Last Login': '🕒',
    'Date Joined': '📅',
    'Code':'🆔',
    'Gender': '⚧️ ',
    'CPF': '📋',
    'CNPJ': '📋',
    'IE': '📋',
    'IM': '📋',
    'Postcode': '📮',
    'City': '🏙️ ',
    'State': '🗺️ ',
    'Address': '📍',
    'Amount Spent': '💸',
    'Number Of Orders': '🛒',
    'Created At': '📅',
    'Updated At': '🕒',
}


def _format_contact(
        obj: DepocObject,
        title: str,
        update: bool = False,
    ):

    if hasattr(obj, 'alias'):
        table_title = obj.alias
        caption = 'customer'
    elif hasattr(obj, 'trade_name'):
        table_title = obj.trade_name
        caption = 'supplier'

    table = Table(
        show_header=True,
        show_footer=True,
        box=None,
        expand=True,
        title=table_title,
        title_justify='right',
        caption=caption,
        caption_justify='right'
    )

    table.add_column('', justify='left', no_wrap=True)
    table.add_column('', justify='left', no_wrap=True)

    data = obj.to_dict()
    data.pop('id', None)
    data.pop('name', None)
    data.pop('alias', None)
    data.pop('legal_name', None)
    data.pop('trade_name', None)
    data.pop('notes', None)

    for k, v in data.items():
        if k in ('last_login', 'date_joined', 'created_at'):
            v = v[:10] if v is not None else 'null'

        k = k.replace('_', ' ').title()
        k = k.replace('Is ', '')
        k = k.upper() if k in ('Cpf', 'Cnpj', 'Ie', 'Im') else k
        
        if v and obj.is_active:
            table.add_row(f'{emojis[k]} {k}: ', f'{v}')
    
    group = Group(table)

    if obj.notes:
        notes = Table(
            show_header=False,
            show_footer=True,
            box=None,
            expand=True,
            title=obj.notes,
            title_justify='center',
        )
        notes.add_column('', justify='left', no_wrap=True)
        group = Group(table, notes)

    if update:
        style = 'green'
        panel_title = f'[bold][green]{title}'
        subtitle = f'[green]{obj.id}'
    elif not obj.is_active:
        style = 'bright_red'
        panel_title = f'[bold][bright_red]{title}'
        subtitle = f'[bright_red]{obj.id}'
    else:
        style = 'none'
        panel_title = f'[bold]{title}'
        subtitle = f'[blue]{obj.id}'

    profile = Panel(
        group,
        title=panel_title,
        title_align='left', 
        subtitle=subtitle,
        subtitle_align='left',
        style=style
    )

    console.print(profile)



def _format_profile(
        obj: DepocObject,
        title: str,
        columns: int = 2,
        update: bool = False,
        delete: bool = False,
    ):
    table = Table(show_header=True, show_footer=True, box=None, expand=True)

    for _ in range(columns):
        table.add_column('', justify='left', no_wrap=True)

    data = obj.to_dict()

    for k, v in data.items():
        if k in ('last_login', 'date_joined'):
            v = v[:10] if v is not None else 'null'

        k = k.replace('_', ' ').title()
        k = k.replace('Is ', '')
        k = k.upper() if k == 'Id' else k
        
        table.add_row(f'{emojis[k]} {k}: ', f'{v}')

    if update:
        style = 'green'
    elif delete:
        style = 'red'
    else:
        style = 'none'

    profile = Panel(table, title=f'[bold]{title}', title_align='left', style=style)

    console = Console()
    console.print(profile)


def _format_response(
        obj: DepocObject,
        title: str,
        header: str,
        highlight: str | None = None,
        color: Literal[
            'red',
            'green',
            'yellow',
            'blue',
            'magenta',
            'cyan',
        ] = 'yellow',
        remove: list[str] | None = None,
    ):
    
    try:
        if obj.is_active == False:
            color = 'red'
    except AttributeError:
        pass

    title = click.style(f'{title.upper():-<50}', fg=color, bold=True)
    header = click.style(f'\n{header:>50}', bold=True)

    if highlight:
        if len(highlight) > 50:
            highlight = highlight[:50] if len(highlight) > 50 else None
        highlight = click.style(f'\n{highlight:>50}', bold=True)

    data = obj.to_dict()
    body: str = ''

    if remove:
        for item in remove:
            data.pop(item)

    for k, v in data.items():
        k = k.replace('_', ' ').title()
        k = k.upper() if k == 'Id' else k

        if isinstance(v, DepocObject):
            if hasattr(v, 'name'):
                v = v.name

        body += f'\n{k}: {v}'

    response = (
        f'{title}'
        f'{header}'
        f'{highlight if highlight else ''}'
        f'{body}'
    )
    click.echo(response)


def spinner() -> None:
    spinner_cycle = itertools.cycle(['-', '\\', '|', '/'])
    for _ in range(20):
        sys.stdout.write(f'\rDeleting {next(spinner_cycle)} ')
        sys.stdout.flush()
        time.sleep(0.1)
    click.echo('')


def page_summary(response: DepocObject):
    total_pages = math.ceil(response.count / 50)
    results_count = len(response.results)
    current_page_number = 1

    if response.next:
        next_page_number = response.next[-1]
        current_page_number = int(next_page_number) - 1
    elif response.previous and not response.next:
        current_page_number = total_pages

    message = (
        f'\n[Page {current_page_number}/{total_pages}] '
        f'Showing {results_count} results (Total: {response.count})\n'
    )

    click.echo(message)
