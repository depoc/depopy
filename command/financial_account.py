import depoc
import click
import sys

from typing import Any

from depoc.utils._error import APIError


@click.command(help='Manage bank account')
@click.option('-b', '--balance', is_flag=True, help='Get total balance')
@click.option('-c', '--create', is_flag=True, help='Create a new bank account')
@click.option('-g', '--get', is_flag=True, help='Get all active bank accounts')
@click.option('-u', '--update', is_flag=True, help='Perform an update')
@click.option('-d', '--delete', is_flag=True, help='Delete bank account')
@click.option('-a', '--activate', is_flag=True, help='Activate a bank account')
@click.option(
    '--name',
    default=None, 
    help='Specify a new name when using -c (create)',
)
@click.option(
    '--id',
    default=None, 
    help='Specify an id when using -a (activate)',
)
@click.pass_context
def banks(
    ctx,
    balance: bool,
    get: bool,
    create: bool,
    update: bool,
    delete: bool,
    activate: bool,
    name: str,
    id: str,
) -> None:

    if not any([balance, get, create, update, delete, activate]):
        click.echo(ctx.get_help())
    
    try:
        client = depoc.DepocClient()
        banks = client.financial_accounts.all()
    except APIError as e:
        click.echo(str(e))
        sys.exit(0)

    if balance:
        total: float = 0
        for bank in banks.results:
            if bank.is_active:
                total += float(bank.balance)
        click.echo(f'Total Balance: ${total:.2f}')

    elif get:
        for bank in banks.results:
            if bank.is_active:
                msg = click.style(f'{bank.name.upper():-^50}', bold=True)
                id_ = click.style(f'\nID: {bank.id}', fg='yellow')
                record = (
                    f'{msg}'
                    f'\nBalance: ${bank.balance}'
                    f'{id_}'
                    f'\nCreated At: {bank.created_at}'
                    '\n'
                )
                click.echo(record)
            else:
                msg = click.style(f'{'DEACTIVATED':-^50}', bold=True)
                id_ = click.style(f'\nID: {bank.id}', fg='red')
                line = click.style(f'\n{'-' * 50}', bold=True)
                record = (
                    f'{msg}'
                    f'{id_} \nName: {bank.name}'
                    f'{line}'
                )
                click.echo(record)

    elif create and name:
        try:
            create_bank = client.financial_accounts.create({'name': name})
            record = (
                f'{'-' * 50}'
                f'\nID: {create_bank.id} '
                f'\nName: {create_bank.name}'
                f'\nBalance: {create_bank.balance}'
                f'\nCreated At: {create_bank.created_at}'
                f'\nIs Active? {create_bank.is_active}'
                f'\n{'-' * 50}'
            )
            click.echo(record)
        except APIError as e:
            click.echo(str(e))
    elif create and not name:
        click.echo('Inform a name for the bank: \n"depoc banks -c --name ____"')


    elif update:
        for idx, bank in enumerate(banks.results, start=1):
            message = (
                f'{idx}. {bank.name}'
                f'\n{'-' * 50}'
            )
            click.echo(message)

        while True:
            try:
                select = int(input('Select a bank account to update: '))
                selected_bank = banks.results[select-1]
                change_name = str(input('Choose a new name for the bank: '))
                break
            except ValueError:
                click.echo('\nInvalid input: \nOnly integers are accepted.\n')
            except IndexError:
                message = (
                    '\nInvalid selection:'
                    '\nChoose a valid number corresponding to the bank.'
                    '\n'
                )
                click.echo(message)

        try:
            data: dict[str, Any] = {'name': change_name}
            update_bank = client.financial_accounts.update(data, selected_bank.id)
            record = (
                f'\nRECORD UPDATED'
                f'\n{'-' * 50}'
                f'\nID: {update_bank.id} '
                f'\nName: {update_bank.name}'
                f'\nBalance: {update_bank.balance}'
                f'\nCreated At: {update_bank.created_at}'
                f'\nIs Active? {update_bank.is_active}'
                f'\n{'-' * 50}'
            )
            click.echo(record)
        except APIError as e:
            click.echo(str(e))

    elif delete:
        for idx, bank in enumerate(banks.results, start=1):
            message = (
                f'{idx}. {bank.name}'
                f'\n{'-' * 50}'
            )
            click.echo(message)

        while True:
            try:
                select = int(input('Select a bank account to delete: '))
                selected_bank_id = banks.results[select-1].id
                break
            except ValueError:
                click.echo('\nInvalid input: \nOnly integers are accepted.\n')
            except IndexError:
                message = (
                    '\nInvalid selection:'
                    '\nChoose a valid number corresponding to the bank.'
                    '\n'
                )
                click.echo(message)

        confirmation = input('Proceed to account deletion? [y/n] ')

        while True:
            if confirmation == 'y':
                try:
                    client.financial_accounts.delete(selected_bank_id)
                    click.echo('Bank account deactivated')
                except APIError as e:
                    click.echo(str(e))
                break
            elif confirmation == 'n':
                break
            else:
                confirmation = input('Proceed to account deletion? [y/n] ')

    elif activate and id:
        try:
            client.financial_accounts.update({'is_active': True}, id)
            click.echo(f'Bank account activated')
        except APIError as e:
            click.echo(str(e))
    elif activate and not id:
        click.echo('Inform the bank id: \n"depoc banks -a --id ____"')
