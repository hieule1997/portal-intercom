from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
import json
from django.utils import timezone
from django.views import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
import threading
import django_rq
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from client import models
from superadmin.forms import UserForm, UserResetForm, get_user_email, ResetForm
from superadmin.tokens import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage
from superadmin.models import MyUser
from django.contrib.auth.models import User

# Create your views here.

q = django_rq.get_queue('default', default_timeout=900)

def direct(request):
    return redirect('client:login')

class EmailThread(threading.Thread):
    def __init__(self, email):
        threading.Thread.__init__(self)
        self._stop_event = threading.Event()
        self.email = email
    
    def run(self):
        self.email.send()

# Login 
def user_login(request):
    user = request.user

    if request.method == 'POST':
        if 'uemail' in request.POST:
            form = UserResetForm(request.POST)
            if form.is_valid():
                to_email = form.cleaned_data['uemail']
                current_site = get_current_site(request)
                user = get_user_email(to_email)
                mail_subject = 'Reset password account.'
                message = render_to_string('client/reset-password.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                    'token': account_activation_token.make_token(user)
                })
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                thread = EmailThread(email)
                thread.start()
                return render(request, 'client/home.html', {'mess': 'Please check mail to reset your password!'})
            else: 
                error = ''
                for field in form:
                    error += field.errors
                return render(request, 'client/home.html', {'error': error})
        elif 'agentname' and 'agentpass' in request.POST:
            username = request.POST.get('agentname')
            password = request.POST.get('agentpass')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    # if user.token_id is None or user.check_expired() == False:
                    return redirect('client:home')
                else: 
                    return render(request, 'client/home.html', {'error': 'Your account has blocked'})
            else:
                return render(request, 'client/home.html', {'error': 'Invalid username or password'})
        elif 'fullname' and 'email' and 'password2' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                current_site = get_current_site(request)
                user = user_form.save()

                mail_subject = 'Active your blog account'
                message = render_to_string('client/active_acc.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.id)).decode(),
                    'token': account_activation_token.make_token(user)
                })
                to_email = user.email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                thread = EmailThread(email)
                thread.start()
                return render(request, 'client/home.html', {'error': 'Check your email to verify'})
            else:
                error = ''
                for field in user_form:
                    error += field.errors
                return render(request, 'client/home.html', {'error': error})
    return render(request, 'client/home.html')

# Reset password
def resetpwd(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64).decode())
        user = MyUser.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data)
                user.save()
                return redirect('/')
            else:
                return redirect('/')
        return render(request, 'client/form-reset-password.html', {})
    else:
        return HttpResponse('Link is valid')

# Checkout
def nations_states(request):
    if request.user.is_authenticated:
        json_data = open('superadmin/static/data/data-nations-states.json')
        data = json.load(json_data)
        return JsonResponse(data, safe=False)
    return redirect('client:login')
# Lấy data timezone từ file json 
def timezone(request):
    if request.user.is_authenticated:
        json_data = open('superadmin/static/data/timezone.json')
        data = json.load(json_data)
        return JsonResponse(data, safe=False)
    return redirect('client:login')

def home(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'client/createvm.html')
    else:
        return HttpResponseRedirect('/')
def setup(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'client/setup.html')
    else:
        return HttpResponseRedirect('/')
def checkout(request):
    user = request.user
    if user.is_authenticated:
        return render(request, 'client/checkout.html')
    else:
        return HttpResponseRedirect('/')
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

# Đăng xuất
def user_logout(request):
    logout(request)
    return redirect('client:login')

# Đăng ký

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = MyUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Bạn đã xác thực email thành công')
    else:
        return HttpResponse('Link kích hoạt không hợp lệ')