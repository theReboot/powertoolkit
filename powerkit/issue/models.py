from django.db import models
from django.core.paginator import Paginator
from django.conf import settings

from modelcluster.fields import ParentalKey

from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


class IssueIndex(Page):
    intro = models.TextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        issues_list = IssuePage.objects.child_of(self).live()
        paginator = Paginator(issues_list, settings.ITEMS_PER_PAGE)
        page = request.GET.get('page', 1)
        context['issues'] = paginator.get_page(page)
        return context

    subpage_types = ['issue.IssuePage']


class IssuePage(Page):
    intro = models.TextField(blank=True, null=True)
    featured_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    #key_players = models.TextField(blank=True, null=True)
    key_players = RichTextField(null=True, blank=True)
    player_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    #policy_background = models.TextField(blank=True, null=True)
    policy_background = RichTextField(null=True, blank=True)
    policy_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('featured_image'),
        FieldPanel('key_players', classname='full'),
        ImageChooserPanel('player_image'),
        FieldPanel('policy_background', classname='full'),
        ImageChooserPanel('policy_image'),
        InlinePanel('issue_points', label='Key Questions'),
    ]

    parent_page_types = ['issue.IssueIndex']


@register_snippet
class Point(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField(blank=True, null=True)

    panels = [
        FieldPanel('question'),
        FieldPanel('answer'),
    ]

    def __str__(self):
        return self.question


class IssuePoint(Orderable, models.Model):
    page = ParentalKey(
        'issue.IssuePage',
        on_delete=models.CASCADE,
        related_name='issue_points'
    )
    point = models.ForeignKey(
        'issue.Point',
        on_delete=models.CASCADE,
        related_name='+'
    )

    class Meta:
        verbose_name = 'Issue point'
        verbose_name_plural = 'Issue points'

    panels = [
        SnippetChooserPanel('point')
    ]
