from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, UserPicture


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
        )


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'bio',
            'image'
        )


class EditPictureForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ('picture',)
