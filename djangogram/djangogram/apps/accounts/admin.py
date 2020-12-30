from django.contrib import admin
from .models import UserProfile, UserPicture


admin.site.register(UserProfile)
admin.site.register(UserPicture)
