from contact.models import Contact


def contact_info(request):
    contacts = Contact.objects.all()
    if contacts:
        return {
            'intro': contacts[0].intro,
            'email': contacts[0].email,
            'phone': contacts[0].phone,
            'address': contacts[0].address
        }
    else:
        return {
            'email': '',
            'phone': '',
            'address': ''
        }
