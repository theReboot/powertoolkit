from django import template
from home.models import FooterText
from issue.models import IssuePage
from contact.models import Contact

register = template.Library()


@register.inclusion_tag('home/footer.html')
def footer():
    _contacts = Contact.objects.all()
    if _contacts:
        _contact = _contacts[0]
    else:
        _contact = {
            'intro': '',
            'phone': '',
            'email': '',
            'address': ''
        }
        
        # _footers = _contact.intro
        # _email = _contact.email
        # _phone = _contact.phone
        # _address = _contact.address
        return

    # _footers = FooterText.objects.all()
    # if _footers:
    #     footer_text = _footers[0].text
    return {
        'contact': _contact,
        'issues': IssuePage.objects.all()
    }
