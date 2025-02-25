import json
import depoc
import click
import getpass

from depoc.utils._error import APIError


@click.command(help='Enter your account')
def login() -> None :
    username = input('username: ')
    password = getpass.getpass('password: ')
    auth = depoc.Connection(username, password)
    
    try:
        depoc.token = auth.token
        client = depoc.DepocClient()
        me = client.me.get()
        click.echo(f'Welcome {me.name}!')

        with open('.token.json', 'w') as f:
            json.dump({'token': auth.token}, f)
            
    except APIError as e:
        click.echo(str(e.message))
        

@click.command(help='Logout of your account')
def logout() -> None:
    with open('.token.json', 'w') as f:
        json.dump({'token': None}, f)


@click.command(help="Get the current user's data")
def me() -> None:
    try:
        client = depoc.DepocClient()
        me = client.me.get()
        record = (
            f'ID: {me.id}'
            f'\nName: {me.name}'
            f'\nEmail: {me.email}'
            f'\nUsername: {me.username}'
            f'\nIs Active?: {me.is_active}'
            f'\nIs Staff?: {me.is_staff}'
            f'\nIs Superuser?: {me.is_superuser}'
            f'\nLast Login: {me.last_login}'
            f'\nDate Joined: {me.date_joined}'
        )
        click.echo(record)
    except APIError as e:
        click.echo(str(e))
