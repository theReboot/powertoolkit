from django.http import JsonResponse

from stats.models import MeteringStatus


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
