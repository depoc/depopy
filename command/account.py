import depoc
import click

from typing import Any

from depoc.utils._error import APIError


@click.command(help='Manage user account')
@click.option('-u', '--update', is_flag=True, help='Perform an update')
@click.option('-d', '--delete', is_flag=True, help='Delete account')
@click.option('--name')
@click.option('--email')
@click.option('--username')
@click.pass_context
def account(
    ctx,
    update: bool,
    delete: bool,
    name: str,
    email: str,
    username: str,
) -> None:
    if not any([update, delete]):
        click.echo(ctx.get_help())
    
    client = depoc.DepocClient()

    if update:
        data: dict[str, Any] = {}

        if name:
            data.update({'name': name})
        if email:
            data.update({'email': email})
        if username:
            data.update({'username': username})

        try:
            update_acccount = client.accounts.update(data)
            record = (
                f'\nID: {update_acccount.id}'
                f'\nName: {update_acccount.name}'
                f'\nEmail: {update_acccount.email}'
                f'\nUsername: {update_acccount.username}'
                f'\nIs Active?: {update_acccount.is_active}'
                f'\nIs Staff?: {update_acccount.is_staff}'
                f'\nIs Superuser?: {update_acccount.is_superuser}'
                f'\nLast Login: {update_acccount.last_login}'
                f'\nDate Joined: {update_acccount.date_joined}'
            )
            click.echo(f'Record updated: {record}')
        except APIError as e:
            click.echo(str(e))
    elif delete:
        confirmation = input('Proceed to account deletion? [y/n] ')

        while True:
            if confirmation == 'y':
                try:
                    client.accounts.delete()
                    click.echo('Account deactivated')
                except APIError as e:
                    click.echo(str(e))
                break
            elif confirmation == 'n':
                break

            confirmation = input('Proceed to account deletion? [y/n] ')
