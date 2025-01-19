from rest_framework.request import Request
from tasks.models import Task


def filter_by_posted(request: Request):
    posted_parameter = request.query_params.get('posted', None) 
    if posted_parameter:
        return Task.objects.filter(posted=True)
    return Task.objects.all()
