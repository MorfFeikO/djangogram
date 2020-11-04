from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm, LoginForm


UserModel = get_user_model()


def signup(request):
    if request.method == 'GET':
        return render(request, 'gram/signup.html')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        print(form.errors.as_data())
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your DJANGOGRAM account'
            message = render_to_string('gram/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete registration')
        else:
            return HttpResponse('FORM IS NOT VALID. Please Try again!')
    else:
        form = SignUpForm()
        return render(request, 'gram/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account')
    else:
        return HttpResponse('Activation link is invalid!')


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        print(form.errors.as_data())
        if form.is_valid():
            return render(request, 'gram/profile.html')
    else:
        form = LoginForm()
        return render(request, 'gram/login.html', {'form': form})


def profile(request):
    return render(request, 'gram/profile.html')


def profile_edit(request):
    return HttpResponse('Profile edit page')
