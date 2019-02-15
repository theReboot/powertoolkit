from django.contrib import admin

from stats.models import PerformanceSummary, PerformanceDetail,\
    RemittanceSummary, RemittanceDetail, GenerationSummary, GenerationDetail


@admin.register(PerformanceSummary)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['month', 'year']

    #def save_model(self, request, obj, form, change):
    #    obj.save()

    #    #import pdb;pdb.set_trace()
    #    #f = open(obj.csv_file.path)
    #    book = xlrd.open_workbook(obj.csv_file.path)
    #    sheet = book.sheet_by_index(0)
    #    lines = []
    #    for rowx in range(1, sheet.nrows):
    #        cols = sheet.row_values(rowx)
    #        lines.append(cols)
    #        PerformanceDetail.objects.create(
    #            summary=obj,
    #            date=xlrd.xldate_as_datetime(cols[0], 0),
    #            disco_consumption=cols[1],
    #            evacuated_energy=cols[2],
    #            system_loss=cols[3],
    #            efficiency=cols[4],
    #            inefficiency=cols[5]
    #        )


        #field_names = ['date', 'consumption', 'evacuated', 'loss', 'efficiency', 'inefficiency']
        #reader = csv.DictReader(f, fieldnames=field_names)
        #for line in reader:
        #    PerformanceDetail.objects.create(
        #        summary=obj,
        #        date=line['date'],
        #        disco_consumption=line['consumption'],
        #        evacuated_energy=line['evacuated'],
        #        system_loss=line['loss']
        #    )
        #fd = form.cleaned_data['csv_file'].read().decode('utf-8')
        #lines = fd.split()
        #reader = csv.DictReader(lines, fieldnames=field_names)
        #for line in reader:
        #    import pdb;pdb.set_trace()
        #reader = csv.reader(open(content=fd))


@admin.register(PerformanceDetail)
class PerformanceDetailAdmin(admin.ModelAdmin):
    list_display = ['summary', 'date', 'disco_consumption',
                    'evacuated_energy', 'system_loss']


@admin.register(RemittanceSummary)
class RemittanceAdmin(admin.ModelAdmin):
    list_display = ['month', 'year']


@admin.register(RemittanceDetail)
class RemittanceDetailAdmin(admin.ModelAdmin):
    list_display = ['summary', 'disco', 'invoice_value', 'disco_payment',
                    'performance_ratio', 'loss', 'inefficiency_ratio']


@admin.register(GenerationSummary)
class GenerationAdmin(admin.ModelAdmin):
    list_display = ['month', 'year']


@admin.register(GenerationDetail)
class GenerationDetailAdmin(admin.ModelAdmin):
    list_display = ['summary', 'date', 'hourly_generation', 'daily_generation',
                    'hourly_losses', 'daily_losses', 'constrained_value',
                    'peak_energy']
