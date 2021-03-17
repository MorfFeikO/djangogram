from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from django.http import JsonResponse
from django.forms.models import model_to_dict

from sendgrid import SendGridAPIClient
from sendgrid import Mail, Email, To, Content

from .models import UserProfile, UserPicture, Friend
from .forms import SignUpForm, EditProfileForm, EditUserProfileForm, EditPictureForm

import json
import environ

UserModel = get_user_model()

env = environ.Env()
environ.Env.read_env()


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your DJANGO_GRAM account'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')

                # added debug=true
            debug = env.bool('DEBUG')
            if debug:
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
            else:
                # added debug=true

                # Adding sendgrid
                sg = SendGridAPIClient(api_key=env.str('SENDGRID_API_KEY'))
                mail = Mail(
                    from_email=Email(env.str('EMAIL_HOST_USER')),
                    to_emails=To(to_email),
                    subject=mail_subject,
                    html_content=Content(mime_type='text/html', content=message)
                )
                sg.client.mail.send.post(request_body=mail.get())
                # Adding sendgrid

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
        error_msg = {'Error': 'The activation link is invalid'}
        return render(request, 'accounts/errors.html', {'e': error_msg})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        u_form = EditUserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid() and u_form.is_valid():
            form.save()
            u_form.save()
            return redirect(reverse('accounts:profile_page'))
        else:
            e = dict(form.errors)
            return render(request, 'accounts/errors.html', {'e': e})
    else:
        form = EditProfileForm(instance=request.user)
        u_form = EditUserProfileForm(instance=request.user.userprofile)
        args = {'form': form, 'u_form': u_form}
        return render(request, 'accounts/edit_profile.html', args)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect(reverse('accounts:profile_page'))
        else:
            return redirect(reverse('accounts:change_password'))
    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}
        return render(request, 'accounts/change_password.html', args)


@login_required
def home(request):
    friend = Friend.objects.get_or_create(current_user=request.user)
    friends = friend[0].users.all()
    users = User.objects.exclude(id=request.user.id).exclude(id__in=friends)

    user_pictures_list = UserPicture.objects.\
        exclude(user__in=users).\
        order_by('-pub_date')

    args = {
        'auth_user': request.user,
        'users': users,
        'pictures': user_pictures_list
    }
    return render(request, 'accounts/home.html', args)


@login_required
def new_profile_view(request, pk=None):
    if request.method == 'GET':
        form = EditPictureForm()

        if pk:
            user = User.objects.get(pk=pk)
        else:
            user = request.user

        user_pictures_list = UserPicture.objects.filter(user=user).order_by('-pub_date')

        auth_friend = Friend.objects.get_or_create(current_user=request.user)
        auth_friends = auth_friend[0].users.all()

        friend = Friend.objects.get_or_create(current_user=user)
        friends = friend[0].users.all()

        if user in auth_friends:
            is_friend = True
        else:
            is_friend = False

        args = {
            'auth_user': request.user,
            'pk': pk,
            'user': user,
            'friends': friends,
            'pictures': user_pictures_list,
            'form': form,
            'is_friend': is_friend,
        }
        return render(request, 'accounts/profile_page.html', args)
    else:
        form = EditPictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            return JsonResponse({'picture': model_to_dict(form)}, status=200)
        else:
            e = dict(form.errors)
            return render(request, 'accounts/errors.html', {'e': e})


@login_required
def operation_with_friends(request, pk, operation, picture_id=None):
    auth_user = request.user
    friend = User.objects.get(pk=pk)

    if request.method == 'POST':
        if operation == 'like':
            picture = get_object_or_404(UserPicture, id=picture_id)
            picture.likes.add(request.user)
            return JsonResponse({'like': picture.total_likes(),
                                 'pk': pk,
                                 'operation': operation,
                                 'picture_id': picture_id},
                                status=200)
        elif operation == 'dislike':
            picture = get_object_or_404(UserPicture, id=picture_id)
            picture.likes.remove(request.user)
            return JsonResponse({'like': picture.total_likes(),
                                 'pk': pk,
                                 'operation': operation,
                                 'picture_id': picture_id},
                                status=200)
        elif operation == 'add':
            Friend.make_friend(auth_user, friend)
            return JsonResponse({'success': 'success'}, status=200)
        elif operation == 'remove':
            Friend.lose_friend(auth_user, friend)
            return JsonResponse({'success': 'success'}, status=200)
