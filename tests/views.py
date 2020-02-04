from django.http import HttpResponse
from django.template import RequestContext, Template


def index(request):
    return HttpResponse(Template("").render(RequestContext(request, {'a': 1000})))
