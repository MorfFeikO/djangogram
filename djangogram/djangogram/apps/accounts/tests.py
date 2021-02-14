from django.test import TestCase, Client
from django.urls import reverse, resolve
from unittest import skip
import io

from PIL import Image

from .views import edit_profile, signup, change_password, home, new_profile_view, operation_with_friends
from .models import UserPicture, UserProfile, User, Friend
from .forms import EditPictureForm, EditProfileForm, EditUserProfileForm, SignUpForm


@skip
class TestUrls(TestCase):

    def test_home_resolved(self):
        url = reverse('accounts:home')
        self.assertEqual(resolve(url).func, home)

    def test_signup_resolved(self):
        url = reverse('accounts:signup')
        self.assertEqual(resolve(url).func, signup)

    def test_change_password_resolved(self):
        url = reverse('accounts:change_password')
        self.assertEqual(resolve(url).func, change_password)

    def test_edit_profile_resolved(self):
        url = reverse('accounts:edit_profile')
        self.assertEqual(resolve(url).func, edit_profile)

    def test_profile_page_resolved(self):
        url = reverse('accounts:profile_page')
        self.assertEqual(resolve(url).func, new_profile_view)

    def test_profile_page_friend_resolved(self):
        url = reverse('accounts:profile_page_friend', kwargs={'pk': '2'})
        self.assertEqual(resolve(url).func, new_profile_view)

    def test_operation_resolved(self):
        url = reverse('accounts:operation', kwargs={'pk': '2', 'operation': 'add'})
        self.assertEqual(resolve(url).func, operation_with_friends)

    def test_like_resolved(self):
        url = reverse('accounts:like', kwargs={'pk': '2', 'operation': 'like', 'picture_id': '5'})
        self.assertEqual(resolve(url).func, operation_with_friends)


class TestForms(TestCase):
    pass


class TestModels(TestCase):
    pass


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.test_user_auth = User(
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

        self.assertRedirects(response, reverse('accounts:profile_page'), status_code=302)

    def test_edit_profile_POST_false(self):
        response = self.client.post(reverse('accounts:edit_profile'), {
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/errors.html')

    def test_change_password_GET(self):
        response = self.client.get(reverse('accounts:change_password'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/change_password.html')

    def test_change_password_POST_true(self):
        response = self.client.post(reverse('accounts:change_password'), {
            'old_password': 'test_password_1',
            'new_password1': 't@st_new_p"ssw0rd',
            'new_password2': 't@st_new_p"ssw0rd'
        })

        self.assertRedirects(response, reverse('accounts:profile_page'), status_code=302)

    def test_change_password_POST_false(self):
        response = self.client.post(reverse('accounts:change_password'), {
            'old_password': 'test_password_1',
            'new_password1': 'test_password_2',
            'new_password2': 'test_password_3'
        })

        self.assertRedirects(response, reverse('accounts:change_password'), status_code=302)

    def test_home_GET(self):
        User.objects.create(
            email='test_admin@gmail.com',
            username='admin',
            password='test_password_3'
        )

        response = self.client.get(reverse('accounts:home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/home.html')

    def test_profile_page_GET(self):
        response = self.client.get(reverse('accounts:profile_page'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_page.html')

    def test_profile_page_GET_with_pk(self):
        user = User.objects.get(username='test_username_2')
        response = self.client.get(reverse('accounts:profile_page_friend', kwargs={'pk': user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_page.html')

    def test_profile_page_GET_with_friend(self):
        auth_user = User.objects.get(username='test_username_1')
        user = User.objects.get(username='test_username_2')
        friend = Friend.objects.get_or_create(current_user=auth_user)
        friend[0].users.add(user)

        response = self.client.get(reverse('accounts:profile_page_friend', kwargs={'pk': user.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile_page.html')

    def test_profile_page_POST_true(self):
        photo_file = self.generate_photo_file()
        data = {
            'picture_title': 'Test title for the picture!',
            'picture': photo_file
        }
        response = self.client.post(reverse('accounts:profile_page'), data, format='multipart')

        self.assertRedirects(response, reverse('accounts:profile_page'), status_code=302)

    def test_profile_page_POST_false(self):
        response = self.client.post(reverse('accounts:profile_page'), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/errors.html')

    def test_operations_with_friends_GET_add_resolved(self):
        response = self.client.get(reverse('accounts:operation', kwargs={'pk': 2, 'operation': 'add'}))

        self.assertEqual(response.status_code, 302)

    def test_operations_with_friends_GET_remove_resolved(self):
        response = self.client.get(reverse('accounts:operation', kwargs={'pk': 2, 'operation': 'remove'}))

        self.assertEqual(response.status_code, 302)

    @skip
    def test_operations_with_friends_GET_like_resolved(self):
        photo_file = self.generate_photo_file()
        user = User.objects.get(username='test_username_2')
        pic = UserPicture(picture_title='Test title for the picture!', picture=photo_file)
        pic.user = user
        pic.save()
        response = self.client.get(reverse('accounts:like', kwargs={'pk': user.pk,
                                                                    'operation': 'like',
                                                                    'picture_id': pic.id
                                                                    }))

        self.assertEqual(response.status_code, 302)

    @skip
    def test_operations_with_friends_GET_dislike_resolved(self):
        pass

