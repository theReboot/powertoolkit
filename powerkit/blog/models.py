from django.db import models
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth.models import User

from modelcluster.fields import ParentalKey

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel,\
    InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class BlogIndex(Page):
    intro = models.TextField(null=True, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        blog_entries = BlogPage.objects.child_of(self).live(
            ).exclude(featured=True).order_by('-date')
        paginator = Paginator(blog_entries, settings.ITEMS_PER_PAGE)
        page = request.GET.get('page', 1)
        context['blog_entries'] = paginator.get_page(page)
        #import pdb;pdb.set_trace()

        #context['blog_entries'] = BlogPage.objects.child_of(
        #    self).live().exclude(featured=True).order_by('-date')
        featured = BlogPage.objects.child_of(
            self).live().filter(featured=True).order_by('-date')
        if featured:
            context['featured'] = featured.first()
        return context

    subpage_types = ['blog.BlogPage']


class BlogPage(Page):
    intro = models.TextField(blank=True, null=True)
    body = RichTextField()
    author = models.CharField(max_length=250, blank=True, null=True)
    #author = models.ForeignKey(
    #    User,
    #    null=True,
    #    blank=True,
    #    on_delete=models.SET_NULL
    #)
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
        FieldPanel('author', classname='full'),
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
