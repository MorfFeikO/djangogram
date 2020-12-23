from django.test import TestCase, Client
from unittest import skip
from django.utils import timezone

from djangogram.djangogram.apps.accounts.models import UserPicture, UserProfile, User


class TestModels(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            email='a.s.bozbei@gmail.com',
            username='alex',
            password='kulopoplaxan'
        )
        self.user.save()
        self.picture_user = UserPicture.objects.create(
            user=self.user,
            picture_title='None',
            picture=None,
            pub_date=timezone.now()
        )
        self.picture_user.save()
        self.profile_user = UserProfile.objects.create(
            user=self.user,
            bio='None',
            image=None, )

    def test_str_is_equal_to_picture_user_title(self):
        self.assertEqual(str(self.picture_user), self.user.username)

    @skip
    def test_str_is_equal_to_profile_user_title(self):
        self.assertEqual(str(self.profile_user), self.user.username)
