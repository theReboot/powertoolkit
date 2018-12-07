from django import template
from home.models import FooterText
from issue.models import IssuePage

register = template.Library()


@register.inclusion_tag('home/footer.html')
def footer():
    _footers = FooterText.objects.all()
    if _footers:
        footer_text = _footers[0].text
    return {
        'footer_text': footer_text,
        'issues': IssuePage.objects.all()
    }
