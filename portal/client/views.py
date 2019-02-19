from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import threading
import django_rq
# Create your views here.

q = django_rq.get_queue('default', default_timeout=900)
def home(request):
    # user = request.user
    # if user.is_authenticated and user.is_adminkvm == False:
    return render(request, 'client/createvm.html')
    # else:
    #     return HttpResponseRedirect('/')
def setup(request):
    # user = request.user
    # if user.is_authenticated and user.is_adminkvm == False:
    return render(request, 'client/setup.html')
    # else:
    #     return HttpResponseRedirect('/')
def checkout(request):
    # user = request.user
    # if user.is_authenticated and user.is_adminkvm == False:
    return render(request, 'client/checkout.html')
    # else:
    #     return HttpResponseRedirect('/')
class check_ping(threading.Thread):
    def __init__(self, host):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.host = host

    def run(self):
        # response = os.system("ping -n 1 " + self.host)
        response = os.system("ping -c 1 " + self.host)
        if response == 0:
            return True
        else:
            return False
