import xlrd
from django.db import models

from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


class StatsPage(Page):
    intro = models.TextField(blank=True)
    performance = models.ForeignKey(
        'PerformanceSummary',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')
    remittance = models.ForeignKey(
        'RemittanceSummary',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')
    generation = models.ForeignKey(
        'GenerationSummary',
        null=True,
        on_delete=models.SET_NULL,
        related_name='+')

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        SnippetChooserPanel('performance', classname='full'),
        SnippetChooserPanel('remittance', classname='full'),
        SnippetChooserPanel('generation', classname='full'),
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
        return '{} {}'.format(self.get_month_display(), self.year)

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


@register_snippet
class RemittanceSummary(models.Model):
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
        return '{} {}'.format(self.get_month_display(), self.year)

    class Meta:
        verbose_name_plural = 'Remittance Summary'

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
                RemittanceDetail.objects.create(
                    summary=self,
                    disco=cols[0],
                    invoice_value=cols[1],
                    disco_payment=cols[2],
                    performance_ratio=cols[3],
                    loss=cols[4],
                    inefficiency_ratio=cols[5]
                )


class RemittanceDetail(models.Model):
    summary = models.ForeignKey(RemittanceSummary, on_delete=models.CASCADE)
    disco = models.CharField(max_length=50)
    invoice_value = models.DecimalField(max_digits=15, decimal_places=2)
    disco_payment = models.DecimalField(max_digits=15, decimal_places=2)
    performance_ratio = models.DecimalField(max_digits=5, decimal_places=2)
    loss = models.DecimalField(max_digits=15, decimal_places=2)
    inefficiency_ratio = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.disco)


@register_snippet
class GenerationSummary(models.Model):
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
        return '{} {}'.format(self.get_month_display(), self.year)

    class Meta:
        verbose_name_plural = 'Generation Summary'

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
                GenerationDetail.objects.create(
                    summary=self,
                    date=xlrd.xldate_as_datetime(cols[0], 0),
                    hourly_generation=cols[1],
                    daily_generation=cols[2],
                    hourly_losses=cols[3],
                    daily_losses=cols[4],
                    constrained_value=cols[5],
                    peak_energy=cols[6]
                )


class GenerationDetail(models.Model):
    summary = models.ForeignKey(GenerationSummary, on_delete=models.CASCADE)
    date = models.DateField()
    hourly_generation = models.PositiveIntegerField()
    daily_generation = models.PositiveIntegerField()
    hourly_losses = models.PositiveIntegerField()
    daily_losses = models.PositiveIntegerField()
    constrained_value = models.DecimalField(max_digits=15, decimal_places=5)
    peak_energy = models.PositiveIntegerField()

    def __str__(self):
        return self.date.strftime('%d-%b-%Y')
