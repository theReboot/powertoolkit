from django.http import JsonResponse

from system.models import Agency, Genco
from stats.models import Disco  # should be in system...


def get_data(request):
    agencies = [
        {
            'id': agency.id,
            'name': agency.name,
            'description': agency.description
        }
        for agency in Agency.objects.all()]

    gencos = [
        {
            'id': genco.id,
            'name': genco.name,
            'type': genco.kind.name,
            'capacity': genco.capacity,
            'location': genco.location.name
        }
        for genco in Genco.objects.all()]

    discos = [
        {
            'id': disco.id,
            'name': disco.name,
            'location': disco.location
        }
        for disco in Disco.objects.all()]
    return JsonResponse(
        {
            'agencies': agencies,
            'discos': discos,
            'gencos': gencos
        })
