import xlrd
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet


class StatsPage(Page):
    intro = models.TextField(blank=True)
    performance = models.ForeignKey(
        'PerformanceSummary',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]


@register_snippet
class Disco(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('location'),
    ]

    def __str__(self):
        return self.name


@register_snippet
class MeteringStatus(models.Model):
    disco = models.ForeignKey(Disco, on_delete=models.CASCADE)
    total_customers = models.PositiveIntegerField()
    metered_customers = models.PositiveIntegerField()
    year = models.PositiveIntegerField()

    panels = [
        FieldPanel('disco'),
        FieldPanel('total_customers'),
        FieldPanel('metered_customers'),
        FieldPanel('year'),
    ]

    class Meta:
        verbose_name_plural = 'Metering Status'

    def __str__(self):
        return '{} - {}'.format(self.disco, self.year)


#class TransmissionPerformance(models.Model):
#    Jan = 1
#    Feb = 2
#    Mar = 3
#    Apr = 4
#    May = 5
#    Jun = 6
#    Jul = 7
#    Aug = 8
#    Sep = 9
#    Oct = 10
#    Nov = 11
#    Dec = 12
#
#    MONTHS = enumerate(
#        ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
#
#    month = models.IntegerField(choices=MONTHS)
#    year = models.IntegerField()
#    csv_file = models.FileField()
#
#    def __str__(self):
#        return '{} {}'.format(self.month, self.year)
#

@register_snippet
class PerformanceSummary(models.Model):
    Jan = 0
    Feb = 1
    Mar = 2
    Apr = 3
    May = 4
    Jun = 5
    Jul = 6
    Aug = 7
    Sep = 8
    Oct = 9
    Nov = 10
    Dec = 11

    MONTHS = enumerate(
        ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
         'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))

    month = models.IntegerField(choices=MONTHS)
    year = models.IntegerField()
    csv_file = models.FileField()

    panels = [
        FieldPanel('month'),
        FieldPanel('year'),
        FieldPanel('csv_file'),
    ]

    def __str__(self):
        return '{} {}'.format(self.month, self.year)

    class Meta:
        verbose_name_plural = 'Performance Summary'

    def save(self, *args, **kwargs):
        if self.id:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)

            book = xlrd.open_workbook(self.csv_file.path)
            sheet = book.sheet_by_index(0)
            lines = []
            for rowx in range(1, sheet.nrows):
                cols = sheet.row_values(rowx)
                lines.append(cols)
                PerformanceDetail.objects.create(
                    summary=self,
                    date=xlrd.xldate_as_datetime(cols[0], 0),
                    disco_consumption=cols[1],
                    evacuated_energy=cols[2],
                    system_loss=cols[3],
                    efficiency=cols[4],
                    inefficiency=cols[5]
                )


class PerformanceDetail(models.Model):
    summary = models.ForeignKey(
        PerformanceSummary, on_delete=models.CASCADE)
    date = models.DateField()
    disco_consumption = models.FloatField()
    evacuated_energy = models.FloatField()
    system_loss = models.FloatField()
    efficiency = models.FloatField()
    inefficiency = models.FloatField()

    def __str__(self):
        return self.date.strftime('%Y-%m-%d')
