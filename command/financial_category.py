import depoc
import click
import sys

from typing import Any

from depoc.utils._error import APIError


@click.command(help='Manage the financial categories')
@click.option('-c', '--create', is_flag=True, help='Create a new category')
@click.option('-g', '--get', is_flag=True, help='Get all active categories')
@click.option('-u', '--update', is_flag=True, help='Perform an update')
@click.option('-d', '--delete', is_flag=True, help='Delete a category')
@click.option(
    '--name',
    default=None, 
    help='Specify a new name when using -c (create)',
)
@click.option(
    '--parent',
    default=None, 
    help='Specify a parent id when using -c (create)',
)
@click.option(
    '--id',
    default=None, 
    help='Specify an id when using -a (activate) or -d (delete)',
)
@click.pass_context
def category(
    ctx,
    create: bool,
    get: bool,
    update: bool,
    delete: bool,
    name: str,
    parent: str,
    id: str,
) -> None:
    if not any([get, create, update, delete]):
        click.echo(ctx.get_help())

    try:
        client = depoc.DepocClient()
        categories = client.financial_categories.all()
    except APIError as e:
        click.echo(str(e))
        sys.exit(0)

    if not categories.results:
        click.echo('No categories :/')

    elif get and categories.results:
        for category in categories.results:
            if category.is_active:
                msg = click.style(f'{category.name.upper():-^50}', bold=True)
                id_ = click.style(f'\nID: {category.id}', fg='yellow')
                record = (
                    f'{msg}'
                    f'{id_}'
                    f'\nParent: {category.parent}'
                    '\n'
                )
                click.echo(record)
            else:
                msg = click.style(f'{'DEACTIVATED':-^50}', bold=True)
                info = click.style(f'\n{category.name}: {category.id}', fg='red')
                record = (f'{msg}{info}\n')
                click.echo(record)

    elif create and name:
        try:
            data: dict[str, Any] = {'name': name}
            data.update({'parent': parent}) if parent else None
            create_category = client.financial_categories.create(data)
            record = (
                f'{'-' * 50}'
                f'\nID: {create_category.id} '
                f'\nName: {create_category.name}'
                f'\nParent: {create_category.parent}'
                f'\nIs Active? {create_category.is_active}'
                f'\n{'-' * 50}'
            )
            click.echo(record)
        except APIError as e:
            click.echo(str(e))
    elif create and not name:
        click.echo(
            'Inform a name for the category: \n"depoc category -c --name ____"'
        )

    elif update and name or parent:
        if not id:
            click.echo('An ID is necessary to update the category')
            sys.exit(0)

        data = {}
        data.update({'name': name}) if name else None
        data.update({'parent': parent}) if parent else None

        try:
            update_category = client.financial_categories.update(data, id)
            record = (
                f'\nRECORD UPDATED'
                f'\n{'-' * 50}'
                f'\nID: {update_category.id} '
                f'\nName: {update_category.name}'
                f'\nParent: {update_category.parent}'
                f'\nIs Active? {update_category.is_active}'
                f'\n{'-' * 50}'
            )
            click.echo(record)
        except APIError as e:
            click.echo(str(e))
    elif update and not name and not parent:
        msg = (
            'Inform a name or parent to update the category: '
            '\n"depoc category -c --parent ____"'
        )
        click.echo(msg)

    elif delete and id:
        try:
            confirmation = input('Proceed to deletion? [y/n] ')
            while True:
                if confirmation == 'y':
                    try:
                        client.financial_categories.delete(id)
                        click.echo('Category deactivated')
                    except APIError as e:
                        click.echo(str(e))
                    break
                elif confirmation == 'n':
                    break
                else:
                    confirmation = input('Proceed to account deletion? [y/n] ')
        except APIError as e:
            click.echo(str(e))
    elif delete and not id:
        click.echo('Inform the ID of the category you want to delete')
