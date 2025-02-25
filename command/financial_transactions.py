import depoc
import click
import sys

from typing import Any

from depoc.utils._error import APIError


@click.command(help='Manage the financial transactions')
@click.option('-c', '--create', is_flag=True, help='Create a new transaction')
@click.option('-g', '--get', is_flag=True, help='Get all transactions')
@click.option('-u', '--update', is_flag=True, help='Perform an update')
@click.option('-d', '--delete', is_flag=True, help='Delete a transaction')
@click.option('-f', '--filter', is_flag=True, help='Filter transactions')
@click.option('--search', help='Search for transaction')
@click.option('--date', help='Search for transaction by date')
@click.option('--start-date', help='Search for transaction by date')
@click.option('--end-date', help='Search for transaction by date')
@click.option('--limit', help='Limit the results shown')
@click.option('--page', help='Navigate to page <number>')
@click.option(
    '--id',
    default=None, 
    help='Specify an id when using -d (delete)',
)
@click.pass_context
def transaction(
    ctx,
    create: bool,
    get: bool,
    update: bool,
    delete: bool,
    filter: bool,
    search: str,
    date: str,
    start_date: str,
    end_date: str,
    limit: int,
    page: int,
    id: str,
) -> None:
    if not any([get, create, update, delete, filter]):
        click.echo(ctx.get_help())
        sys.exit(0)

    try:
        client = depoc.DepocClient()
        transactions = client.financial_transactions.all()            
        if limit:
            transactions = client.financial_transactions.all(limit=int(limit))
        elif page:
            transactions = client.financial_transactions.all(page=int(page))
        elif limit and page:
            transactions = client.financial_transactions.all(
                limit=int(limit),
                page=int(page),
            )
    except APIError as e:
        click.echo(str(e))
        sys.exit(0)

    if get and transactions.results:
        click.echo(f'\nNumber of transactions: {transactions.count}')
        if transactions.next:
            click.echo(f'Select next page: --page <number>')
        for transaction in transactions.results:
            msg = click.style(f'{transaction.type.upper():-^50}', bold=True)
            id_ = click.style(f'ID: {transaction.id}', fg='yellow')
            line = click.style(f'{'-' * 50}', bold=True)
            record = (
                f'\n{msg}'
                f'\n{id_}'
                '\n'
                f'\nAmount: {transaction.amount}'
                f'\nDescription: {transaction.description}'
                '\n'
                f'\nCategory: {transaction.category.name}'
                f'\nAccount: {transaction.account.name}'
                f'\nContact: {transaction.contact.name}'
                f'\nPayment: {transaction.payment}'
                f'\nOperator: {transaction.operator.name}'
                f'\nLinked: {transaction.linked}'
                '\n'
                f'\n{transaction.timestamp}'
                f'\n{line}'
            )
            click.echo(record)
    elif get and not transactions.results:
        click.echo('No transactions :/')
 
    elif create:
        while True:
            click.echo('\nCredit [c] | Debit [d] | Transfer [t]')
            type = input('Select a type of transaction [c/d/t]: ')
            if type in ('c, d, t'):
                break

        while True:
            try:
                amount = float(input('Amount: $'))
                account = input('Account ID: ')
                if type == 't':
                    send_to = input('Destination Account ID: ')
                description = input('Description: ')
                category = input('Category ID: ')
                contact = input('Contact ID: ')
                payment = input('Payment ID: ')
                linked = input('Linked Transaction ID: ')
                break
            except ValueError:
                click.echo('\nInvalid input: \nOnly integers are accepted.\n')

        transaction_type = None
        if type == 'c':
            transaction_type = 'credit'
        elif type == 'd':
            transaction_type = 'debit'
        elif type == 't':
            transaction_type = 'transfer'

        data: dict[str, Any] = {'type': transaction_type}

        if type == 't':
            data.update({'send_to': send_to}) if send_to else None

        data.update({'amount': amount}) if amount else None
        data.update({'account': account}) if account else None
        data.update({'description': description}) if description else None
        data.update({'category': category}) if category else None
        data.update({'contact': contact}) if contact else None
        data.update({'payment': payment}) if payment else None
        data.update({'linked': linked}) if linked else None

        try:
            create_transaction = client.financial_transactions.create(data)
            msg = click.style(f'{create_transaction.type.upper():-^50}', bold=True)
            id_ = click.style(f'ID: {create_transaction.id}', fg='yellow')
            line = click.style(f'{'-' * 50}', bold=True)
            record = (
                f'\n{msg}'
                f'\n{id_}'
                '\n'
                f'\nAmount: {create_transaction.amount}'
                f'\nDescription: {create_transaction.description}'
                '\n'
                f'\nCategory: {create_transaction.category.name}' # type: ignore
                f'\nAccount: {create_transaction.account.name}' # type: ignore
                f'\nContact: {create_transaction.contact.name}' # type: ignore
                f'\nPayment: {create_transaction.payment}'
                f'\nOperator: {create_transaction.operator.name}' # type: ignore
                f'\nLinked: {create_transaction.linked}'
                '\n'
                f'\n{create_transaction.timestamp}'
                f'\n{line}'
            )
            click.echo(record)
        except APIError as e:
            click.echo(str(e))

    elif delete and id:
        try:
            confirmation = input('Proceed to deletion? [y/n] ')
            while True:
                if confirmation == 'y':
                    try:
                        client.financial_transactions.delete(id)
                        click.echo('Transaction deleted')
                    except APIError as e:
                        click.echo(str(e))
                    break
                elif confirmation == 'n':
                    break
        except APIError as e:
            click.echo(str(e))
    elif delete and not id:
        click.echo('Inform the ID of the transaction you wish to delete')


    elif filter:
        try:
            search_transaction = client.financial_transactions.filter(
                search=search,
                date=date,
                start_date=start_date,
                end_date=end_date,
            )
            if search_transaction:
                click.echo(f'\nTransactions found: {search_transaction.count}')
                if transactions.next:
                    click.echo(f'Select next page: --page <number>')
                for transaction in search_transaction.results:
                    msg = click.style(f'{transaction.type.upper():-^50}', bold=True)
                    id_ = click.style(f'ID: {transaction.id}', fg='yellow')
                    line = click.style(f'{'-' * 50}', bold=True)
                    record = (
                        f'\n{msg}'
                        f'\n{id_}'
                        '\n'
                        f'\nAmount: {transaction.amount}'
                        f'\nDescription: {transaction.description}'
                        '\n'
                        f'\nCategory: {transaction.category.name}'
                        f'\nAccount: {transaction.account.name}'
                        f'\nContact: {transaction.contact.name}'
                        f'\nPayment: {transaction.payment}'
                        f'\nOperator: {transaction.operator.name}'
                        f'\nLinked: {transaction.linked}'
                        '\n'
                        f'\n{transaction.timestamp}'
                        f'\n{line}'
                    )
                    click.echo(record)
        except APIError as e:
            click.echo(str(e))
