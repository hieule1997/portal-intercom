from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
# Create your views here.

def home(request):
    return render(request,'home.html')

# def user_login(request):
    user = request.user
    mess_register_ok = 'Hãy kiểm tra email của bạn để hoàn tất đăng ký'
    if user.is_authenticated  and user.is_adminkvm:
        return HttpResponseRedirect('/home')
    elif user.is_authenticated  and user.is_adminkvm == False:
        return HttpResponseRedirect('/client')
    else:
        if request.method == 'POST':
            # post form để User yêu cầu reset mật khẩu, gửi link về mail
            if 'uemail' in request.POST:
                form = UserResetForm(request.POST)
                if form.is_valid():
                    to_email = form.cleaned_data['uemail']
                    current_site = get_current_site(request)
                    user = get_user_email(to_email)
                    mail_subject = 'Reset password your account.'
                    message = render_to_string('kvmvdi/resetpwd.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    thread = EmailThread(email)
                    thread.start()
                    return render(request, 'kvmvdi/login.html', {'mess': 'Please check email to reset your password!'})
                else:
                    error = ''
                    for field in form:
                        error += field.errors
                    return render(request, 'kvmvdi/login.html', {'error': error})
            elif 'agentname' and 'agentpass' in request.POST:
                username = request.POST['agentname']
                password = request.POST['agentpass']
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active and user.is_adminkvm:
                        print(username)
                        login(request, user)
                        if user.token_id is None or user.check_expired() == False:
                            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                            user.token_id = getToken(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                                        user_domain_id='default', project_domain_id='default')
                            user.save()
                        return HttpResponseRedirect('/home')
                    elif user.is_active and user.is_adminkvm == False:
                        login(request, user)
                        if user.token_id is None or user.check_expired() == False:
                            user.token_expired = timezone.datetime.now() + timezone.timedelta(seconds=OPS_TOKEN_EXPIRED)
                            user.token_id = getToken(ip=OPS_IP, username=user.username, password=user.username,
                                                     project_name=user.username, user_domain_id='default',
                                                     project_domain_id='default')
                            user.save()
                        return HttpResponseRedirect('/client')
                    else:
                        return render(request, 'kvmvdi/login.html',{'error':'Your account is blocked!'})
                else:
                    return render(request, 'kvmvdi/login.html',{'error':'Invalid username or password '})
            elif 'firstname' and 'email' and 'password2' in request.POST:
                user_form = UserForm(request.POST)
                if user_form.is_valid():
                    current_site = get_current_site(request)
                    user = user_form.save()

                    mail_subject = 'Activate your blog account.'
                    message = render_to_string('kvmvdi/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid':urlsafe_base64_encode(force_bytes(user.id)).decode(),
                        'token':account_activation_token.make_token(user),
                    })
                    to_email = user.email
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                    )
                    thread = EmailThread(email)
                    thread.start()
                    return render(request, 'kvmvdi/login.html',{'error':mess_register_ok})
                    
                    # if user.username != 'admin':
                    #     connect = keystone(ip=OPS_IP, username=OPS_ADMIN, password=OPS_PASSWORD, project_name=OPS_PROJECT,
                    #                     user_domain_id='default', project_domain_id='default')
                    #     connect.create_project(name=user.username, domain='default')
                    #     check = False
                    #     while check == False:
                    #         if connect.find_project(user.username):
                    #             connect.create_user(name=user.username, domain='default', project=user.username,
                    #                                 password=user.username, email=request.POST['email'])
                    #             check = True
                    #     check1 = False
                    #     while check1 == False:
                    #         if connect.find_user(user.username):
                    #             check1 = True
                    #     connect.add_user_to_project(user=user.username, project=user.username)
                else:
                    error = ''
                    for field in user_form:
                        error += field.errors
                    return render(request, 'kvmvdi/login.html',{'error':error})
        return render(request, 'kvmvdi/login.html')