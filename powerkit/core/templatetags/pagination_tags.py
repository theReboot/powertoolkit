from django import template


register = template.Library()


@register.inclusion_tag('includes/paginator.html')
def show_pagination(paginator, page_id):
    return {'paginator': paginator, 'page_id': page_id}
