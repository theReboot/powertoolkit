from issue.models import IssuePage


def issues(request):
    issues = IssuePage.objects.all()
    return {'issues': issues}
