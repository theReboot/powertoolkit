from about.models import Metadata


def get_metadata(request):
    meta_data = Metadata.objects.all()
    if meta_data:
        mtd = meta_data[0]
        return {
            'meta_description': mtd.description,
            'meta_keywords': mtd.keywords
        }
    else:
        return {
            'meta_description': '',
            'meta_keywords': ''
        }
