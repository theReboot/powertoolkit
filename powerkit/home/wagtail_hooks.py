from django.utils.safestring import mark_safe
from wagtail.core import hooks


class DownloadPanel:
    order = 50

    def render(self):
        return mark_safe('''
          <section class="panel summary nice-padding second">
            <div><a href="">First Link</a></div>
            <div><a href="">Second Link</a></div>
            <div><a href="">Third Link</a></div>
          </section>
        ''')


@hooks.register('construct_homepage_panels')
def another_welcome_panels(request, panels):
    return panels.append(DownloadPanel())
