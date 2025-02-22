from depoc.resources.methods import Retrieve
from depoc.objects.contact import ContactObject


class Contact(Retrieve[ContactObject]):
    obj = ContactObject
    endpoint = 'contacts'
