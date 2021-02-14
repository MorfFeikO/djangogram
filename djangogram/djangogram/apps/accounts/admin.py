from django.contrib import admin
from .models import UserProfile, UserPicture, Friend


admin.site.register(UserProfile)
admin.site.register(UserPicture)
admin.site.register(Friend)
