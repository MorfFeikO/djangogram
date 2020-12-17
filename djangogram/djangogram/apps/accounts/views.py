from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import SignUpForm, EditProfileForm, EditUserProfileForm, EditPictureForm

UserModel = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():  # валидация формы. Как отловить или наладить, что не так?
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your DJANGOGRAM account'
            message = render_to_string('accounts/acc_active_email.html', {
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
            args = form.errors.as_json()
            return HttpResponse(args)
    else:
        form = SignUpForm()
        return render(request, 'accounts/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/accounts/login/')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required
def view_profile(request):
    args = {'user': request.user}
    return render(request, 'accounts/profile.html', args)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        u_form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            return redirect('/accounts/profile/')
        else:
            args = form.errors.as_json()
            # print(form.errors.as_data())
            return HttpResponse(args)
    else:
        form = EditProfileForm(instance=request.user)
        u_form = EditUserProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'u_form': u_form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def edit_picture(request):
    if request.method == 'POST':
        form = EditPictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse('BINGO')
    else:
        form = EditPictureForm()
        args = {'form': form}
        return render(request, 'accounts/edit_picture.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/profile/')
        else:
            return redirect('/accounts/profile/password/')
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)
