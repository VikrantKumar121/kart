from django.shortcuts import render,redirect
from .models import User
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import requests

#
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):
    """"""
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_no = form.cleaned_data['phone_no']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_name = form.cleaned_data['user_name']

            user = User.objects.create_user(
                first_name = first_name,
                last_name = last_name,
                email = email,
                password = password,
                user_name = user_name
            )

            user.phone_no = phone_no
            user.save()

            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            msg = render_to_string('accounts/verification.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, msg, to=[to_email])
            send_email.send()
            messages.success(request, 'Registration is Successful. Please activate.')
            return redirect('login')


    context = {
        'form': form,
    }

    return render(request,'accounts/register.html', context)

def login(request):
    """"""

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email= email, password= password)

        if user != None:
            auth.login(request, user)
            messages.success(request, 'Login successful')
            url = request.META.get('HTTP_REFERER')
            try :
                query = requests.utils.urlparse(url).query
                # print('query', query)
                params = dict(i.split('=') for i in query.split('&'))
                # print('params', params)
                if params.get('next') != None:
                    nxtPage = params['next']
                    return redirect(nxtPage)
            except:
                return redirect('home')
        else:
            messages.error(request, 'Incorect credentials')

    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    """"""
    auth.logout(request)
    messages.success(request, 'Logout successful')
    return redirect('login')

def activate(request, uidb64, token):
    """"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

@login_required(login_url = 'login')
def dashboard(request):
    """"""
    return render(request, 'accounts/dashboard.html')

def forgot_password(request):
    """"""
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.get(email = email)
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Reset Your Password'
            msg = render_to_string('accounts/resetpassword_validate.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, msg, to=[to_email])
            send_email.send()

            messages.success(request, 'reset link sent!')
            return redirect('login')

        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    return render(request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    """"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user != None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid

        messages.success(request, 'pls reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'Invalid link')
        return redirect('login')
    # return redirect('login')

def reset_password(request):
    """"""
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')

            user = User.objects.get(pk = uid)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
             messages.error(request, 'Password does not match')

    return render(request, 'accounts/resetpassword.html')
