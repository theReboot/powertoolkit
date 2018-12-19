"""powerkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
#from django.views.generic import TemplateView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

from stats import views as stat_views
from system import views as system_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('stats/chart/<int:year>/', stat_views.get_data),
    path('stats/download/<int:year>/', stat_views.download),
    path('system/data/', system_views.get_data),
    #path(
    #    'stats/',
    #    TemplateView.as_view(template_name='stats.html'),
    #    name='stats'
    #),
    #path(
    #    'system/',
    #    TemplateView.as_view(template_name='system.html'),
    #    name='system'
    #),
    #path(
    #    'issues/',
    #    TemplateView.as_view(template_name='issues.html'),
    #    name='issues'
    #),
    #path(
    #    'about/',
    #    TemplateView.as_view(template_name='about.html'),
    #    name='about'
    #),
    #path(
    #    'contact/',
    #    TemplateView.as_view(template_name='contact.html'),
    #    name='contact'
    #),
    #path(
    #    'blog/',
    #    TemplateView.as_view(template_name='blog.html'),
    #    name='blog'
    #),
    # @bayo this is temporary. Please remove when appropriate
    #path(
    #    'blog/long-history-power-management-nigeria/',
    #    TemplateView.as_view(template_name='single-post.html'),
    #    name='testPost'
    #),
    # CMS
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'', include(wagtail_urls)),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Power Toolkit Admin'
