from contact.models import ContactPage


def contact_info(request):
    contacts = ContactPage.objects.all()
    if contacts:
        return {
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
