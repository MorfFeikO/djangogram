from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import UserProfile, UserPicture
from .forms import SignUpForm, EditProfileForm, EditUserProfileForm, EditPictureForm

UserModel = get_user_model()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        # print(form.errors.as_json())
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
            conf_msg = 'Please confirm your email address to complete registration!'
            return render(request, 'accounts/confirmation_signup.html', {'conf_msg': conf_msg})
        else:
            e = dict(form.errors)
            return render(request, 'accounts/errors.html', {'e': e})
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
        return redirect(reverse('accounts:login'))
    else:
        e = dict(form.errors)
        return render(request, 'accounts/errors.html', {'e': e})


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
            return redirect(reverse('accounts:view_profile'))
        else:
            e = dict(form.errors)
            return render(request, 'accounts/errors.html', {'e': e})
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
            return redirect(reverse('accounts:edit_picture'))
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
            return redirect(reverse('accounts:view_profile'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)

# Ниже я все протестировал!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@login_required
def profile_pictures(request):
    picture_list = UserPicture.objects.filter(user=request.user).order_by('-pub_date')
    return render(request, 'accounts/picture_list.html', {'picture_list': picture_list})


@login_required
def profile_list(request):
    user_list = User.objects.order_by('username').all()
    return render(request, 'accounts/user_list.html', {'user_list': user_list})


@login_required
def profile_view(request, username):
    user = User.objects.get(username=username)
    args = {'user': user}
    return render(request, 'accounts/user_profile.html', args)


def home(request):
    return render(request, 'accounts/home.html')


@login_required
def pictures_view(request, username):
    user = User.objects.get(username=username)
    picture_list = UserPicture.objects.filter(user=user).order_by('-pub_date')
    return render(request, 'accounts/picture_list.html', {'picture_list': picture_list})
