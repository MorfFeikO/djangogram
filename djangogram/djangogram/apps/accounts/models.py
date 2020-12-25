from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_image', blank=True)
    bio = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.user.username


class UserPicture(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    picture_title = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='profile_image', blank=True)
    pub_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.picture_title


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)
