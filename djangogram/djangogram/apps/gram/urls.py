from django.urls import path
from . import views


app_name = 'gram'
urlpatterns = [
        path('profile/', views.profile, name="profile"),
        path('profile/edit', views.edit, name="edit"),
        path('signup/', views.signup, name="signup"),
        path('login/', views.login, name="login"),
        path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
