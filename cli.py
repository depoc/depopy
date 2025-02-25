import click

import command.auth
import command.account
import command.financial_account
import command.financial_category
import command.financial_transactions

@click.group()
def main() -> None:
   pass
 
main.add_command(command.auth.login)
main.add_command(command.auth.logout)
main.add_command(command.auth.me)
main.add_command(command.account.account)
main.add_command(command.financial_account.banks)
main.add_command(command.financial_category.category)
main.add_command(command.financial_transactions.transaction)
