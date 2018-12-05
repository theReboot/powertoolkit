from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndex(Page):
    intro = models.TextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context['blog_entries'] = BlogPage.objects.child_of(
            self).live().exclude(featured=True)
        featured = BlogPage.objects.child_of(
            self).live().filter(featured=True)
        if featured:
            context['featured'] = featured.first()
        return context


class BlogPage(Page):
    intro = models.TextField(blank=True, null=True)
    body = RichTextField()
    date = models.DateField("Post date")
    featured = models.BooleanField(default=False)
    feed_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('body'),
        index.FilterField('date'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro', classname='full'),
        FieldPanel('body', classname='full'),
        ImageChooserPanel('feed_image'),
        InlinePanel('related_links', label='Related links'),
    ]

    promote_panels = [
        MultiFieldPanel(Page.promote_panels, 'Common page configuration'),
        FieldPanel('featured'),
    ]

    parent_page_types = ['blog.BlogIndex']
    subpage_types = []


class BlogPageRelatedLink(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name='related_links')
    name = models.CharField(max_length=255)
    url = models.URLField()

    panels = [
        FieldPanel('name'),
        FieldPanel('url'),
    ]
