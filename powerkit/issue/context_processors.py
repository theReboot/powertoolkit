from issue.models import IssuePage


def issues(request):
    issues = IssuePage.objects.live()
    return {'issues': issues}
