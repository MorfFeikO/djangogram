from django.test import TestCase, Client
from django.urls import reverse, resolve
from unittest import skip
import io

from PIL import Image

from .views import view_profile, edit_profile, edit_picture, signup, change_password, home, profile_view,\
    profile_pictures, profile_list, pictures_view
from .models import UserPicture, UserProfile, User
from .forms import EditPictureForm, EditProfileForm, EditUserProfileForm, SignUpForm


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


class TestForms(TestCase):
    pass


class TestModels(TestCase):
    pass


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        # User.objects.create(
        #     email='test_username_1@gmail.com',
        #     username='test_username_1',
        #     password='test_password_1'
        # )

        self.test_user_auth = User.objects.create(
            email='test_username_1@gmail.com',
            username='test_username_1',
        )
        self.test_user_auth.set_password('test_password_1')
        self.test_user_auth.save()
        User.objects.create(
            email='test_username_2@gmail.com',
            username='test_username_2',
            password='test_password_2'
        )

        # self.test_user_auth = User.objects.filter(username='test_username_1').get()
        self.client.force_login(self.test_user_auth)
        self.test_user = User.objects.filter(username='test_username_2').get()

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_signup_GET(self):
        response = self.client.get(reverse('accounts:signup'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/signup.html')

    def test_signup_POST_true(self):
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'test_username_3@gmail.com',
            'username': 'test_username_3',
            'password1': 'test_password_3',
            'password2': 'test_password_3'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/confirmation_signup.html')

    def test_signup_POST_false(self):
        response = self.client.post(reverse('accounts:signup'), {
            'email': 'test_username_3@gmail.com',
            'username': 'test_username_3',
            'password1': 'test_password_3',
            'password2': 'test_password_4'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/errors.html')

    def test_activate_TRY_true(self):
        pass

    def test_activate_TRY_false(self):
        pass

    def test_activate_IF_true(self):
        pass

    def test_activate_IF_false(self):
        pass

    def test_view_profile_GET(self):
        response = self.client.get(reverse('accounts:view_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_edit_profile_GET(self):
        response = self.client.get(reverse('accounts:edit_profile'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_profile.html')

    def test_edit_profile_POST_true(self):
        response = self.client.post(reverse('accounts:edit_profile'), {
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name',
            'bio': 'This is test bio',
            'image': 'None'
        })

        self.assertRedirects(response, reverse('accounts:view_profile'), status_code=302)

    def test_edit_profile_POST_false(self):
        response = self.client.post(reverse('accounts:edit_profile'), {
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/errors.html')

    def test_edit_picture_GET_true(self):
        response = self.client.get(reverse('accounts:edit_picture'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/edit_picture.html')


    def test_edit_picture_POST_true(self):
        photo_file = self.generate_photo_file()
        data = {
            'picture_title': 'Test title for the picture!',
            'picture': photo_file
        }
        response = self.client.post(reverse('accounts:edit_picture'), data, format='multipart')

        self.assertRedirects(response, reverse('accounts:view_profile'), status_code=302)

    @skip
    def test_edit_picture_POST_false(self):
        response = self.client.post(reverse('accounts:edit_picture'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/errors.html')

    def test_change_password_GET(self):
        response = self.client.get(reverse('accounts:change_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    @skip
    def test_change_password_POST_true(self):
        response = self.client.post(reverse('accounts:change_password'), {
            'old_password': 'test_password_1',
            'new_password1': 'test_password_1_new',
            'new_password2': 'test_password_1_new'
        })

        self.assertRedirects(response, reverse('accounts:view_profile'), status_code=302)

    def test_change_password_POST_false(self):
        response = self.client.post(reverse('accounts:change_password'), {
            'old_password': 'test_password_1',
            'new_password1': 'test_password_2',
            'new_password2': 'test_password_3'
        })

        self.assertRedirects(response, reverse('accounts:change_password'), status_code=302)

    def test_profile_pictures_GET(self):
        response = self.client.get(reverse('accounts:picture_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/picture_list.html')

    def test_profile_list_GET(self):
        response = self.client.get(reverse('accounts:user_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_list.html')

    def test_profile_view_GET(self):
        response = self.client.get(reverse('accounts:user_profile',
                                           kwargs={'username': self.test_user.username}
                                           ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/user_profile.html')

    def test_home_GET(self):
        response = self.client.get(reverse('accounts:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')

    def test_pictures_view_GET(self):
        response = self.client.get(reverse('accounts:user_pictures',
                                           kwargs={'username': self.test_user.username}
                                           ))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/picture_list.html')
