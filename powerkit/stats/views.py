from django.http import JsonResponse, HttpResponse

from stats.models import MeteringStatus
from core.excel import download_status_data


def get_data(request, year):
    statuses = MeteringStatus.objects.filter(year=year).order_by('disco')
    years = list(set(s.year for s in MeteringStatus.objects.all()))
    out = [
        {
            'id': status.id,
            'disco': status.disco.name,
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
            status.disco.name.upper(),
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
