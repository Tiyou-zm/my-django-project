from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, Django! Blog应用工作正常！")
