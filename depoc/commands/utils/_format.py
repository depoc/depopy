import click
import sys
import itertools
import time
import math

from typing import Literal

from depoc.objects.base import DepocObject


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

    click.echo(f'\nResults: {response.count}')

    if response.next:
        next_page_number = response.next[-1]
        current_page_number = int(next_page_number) - 1
    elif response.previous and not response.next:
        current_page_number = total_pages

    click.echo(f'Page {current_page_number} out of {total_pages}')
    click.echo(f'Showing {results_count} results on page {current_page_number}')
