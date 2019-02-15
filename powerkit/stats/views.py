from django.http import JsonResponse, HttpResponse

from stats.models import MeteringStatus, StatsPage, PerformanceDetail,\
    RemittanceDetail, GenerationDetail
from core.excel import download_status_data


def get_data(request, year):
    statuses = MeteringStatus.objects.filter(year=year).order_by('disco')
    years = list(set(s.year for s in MeteringStatus.objects.all()))
    out = [
        {
            'id': status.id,
            'disco': status.disco.location,
            'total': status.total_customers,
            'metered': status.metered_customers,
            'year': status.year
        } for status in statuses]
    return JsonResponse(
        {'statuses': out, 'years': years, 'current_year': year})


def download(request, year):
    statuses = MeteringStatus.objects.filter(year=year).order_by('disco')
    data = []
    for idx, status in enumerate(statuses):
        gap = status.total_customers - status.metered_customers
        perc = status.metered_customers * 100 // status.total_customers
        line = [
            idx + 1,
            status.disco.location.upper(),
            status.total_customers,
            status.metered_customers,
            gap,
            '{}%'.format(perc)
        ]
        data.append(line)

    fname = 'metering-status-{}'.format(year)
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheet.sheet')
    response['Content-Disposition'] = 'attachment;filename={}.xlsx'.format(fname)
    download_status_data(data, year, response)
    return response


def get_performance(request):
    page = StatsPage.objects.all()[0]
    details = [
        {
            'id': item.id,
            'date': item.date.strftime('%d-%b-%Y'),
            'disco_consumption': item.disco_consumption,
            'evacuated_energy': item.evacuated_energy,
            'system_loss': item.system_loss,
            'efficiency': item.efficiency,
            'inefficiency': item.inefficiency
        }
        for item in PerformanceDetail.objects.filter(summary=page.performance)]
    return JsonResponse({'performance': details})


def get_remittance(request):
    page = StatsPage.objects.all()[0]
    details = [
        {
            'id': item.id,
            'disco': item.disco,
            'invoice_value': str(item.invoice_value),
            'disco_payment': str(item.disco_payment),
            'performance_ratio': str(item.performance_ratio),
            'loss': str(item.loss),
            'inefficiency_ratio': str(item.inefficiency_ratio)
        }
        for item in RemittanceDetail.objects.filter(summary=page.remittance)]
    return JsonResponse({'remittance': details})


def get_generation(request):
    page = StatsPage.objects.all()[0]
    details = [
        {
            'id': item.id,
            'date': item.date.strftime('%d-%b-%Y'),
            'hourly_generation': item.hourly_generation,
            'daily_generation': item.daily_generation,
            'hourly_losses': item.hourly_losses,
            'daily_losses': item.daily_losses,
            'constrained_value': item.constrained_value,
            'peak_energy': item.peak_energy
        }
        for item in GenerationDetail.objects.filter(summary=page.generation)
    ]
    return JsonResponse({'generation': details})
