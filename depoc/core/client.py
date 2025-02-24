from depoc.services.user import User
from depoc.services.owner import Owner
from depoc.services.account import Account
from depoc.services.business import Business
from depoc.services.customer import Customer
from depoc.services.supplier import Supplier
from depoc.services.contact import Contact
from depoc.services.finance import (
    FinancialAccount,
    FinancialCategory,
    FinancialTransaction,
)
from depoc.services.member import Member
from depoc.services.product import Product, ProductCategory, ProductCost


class DepocClient:
    def __init__(self, token: str | None = None):
        self._token = token
        
        # top-level services
        self.me = User()
        self.owner = Owner()
        self.accounts = Account()
        self.business = Business()
        self.customers = Customer()
        self.suppliers = Supplier()
        self.contacts = Contact()
        self.financial_accounts = FinancialAccount()
        self.financial_categories = FinancialCategory()
        self.financial_transactions = FinancialTransaction()
        self.members = Member()
        self.products = Product()
        self.product_categories = ProductCategory()
        self.product_cost = ProductCost()
        