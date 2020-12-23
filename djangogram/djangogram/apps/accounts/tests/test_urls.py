from django.test import TestCase, Client
from django.urls import reverse, resolve

from djangogram.djangogram.apps.accounts.views import view_profile, edit_profile, edit_picture, signup, \
    change_password, home, profile_view, profile_pictures, profile_list, pictures_view
from djangogram.djangogram.apps.accounts.models import UserPicture, UserProfile, User
from djangogram.djangogram.apps.accounts.forms import EditPictureForm, EditProfileForm, EditUserProfileForm, SignUpForm


class TestUrls(TestCase):

    def test_view_profile_resolved(self):
        url = reverse('accounts:view_profile')
        self.assertEqual(resolve(url).func, view_profile)

    def test_edit_profile_resolved(self):
        url = reverse('accounts:edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_edit_picture_resolved(self):
        url = reverse('accounts:edit_picture')
        self.assertEqual(resolve(url).func, edit_picture)

    def test_signup_resolved(self):
        url = reverse('accounts:signup')
        self.assertEqual(resolve(url).func, signup)

    def test_change_password_resolved(self):
        url = reverse('accounts:change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_home_resolved(self):
        url = reverse('accounts:home')
        self.assertEqual(resolve(url).func, home)

    def test_profile_view_resolved(self):
        self.client = Client()
        User.objects.create(
            email='a.s.bozbei@gmail.com',
            username='alex',
            password='kulopoplaxan'
        )
        user = User.objects.filter(username='alex').get()

        url = reverse('accounts:user_profile', args=[user.username])
        self.assertEqual(resolve(url).func, profile_view)

    def test_profile_pictures_resolved(self):
        url = reverse('accounts:picture_list')
        self.assertEqual(resolve(url).func, profile_pictures)

    def test_profile_list_resolved(self):
        url = reverse('accounts:user_list')
        self.assertEqual(resolve(url).func, profile_list)

    def test_pictures_view_resolved(self):
        self.client = Client()
        User.objects.create(
            email='a.s.bozbei@gmail.com',
            username='alex',
            password='kulopoplaxan'
        )
        user = User.objects.filter(username='alex').get()

        url = reverse('accounts:user_pictures', args=[user.username])
        self.assertEqual(resolve(url).func, pictures_view)
