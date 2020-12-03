from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
        path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
        path('logout/', auth_views.LoginView.as_view(template_name='accounts/logout.html')),
        path('profile/', views.view_profile, name='view_profile'),
        path('profile/edit/', views.edit_profile, name='edit_profile'),
        path('edit/', views.edit_picture, name='edit_picture'),
        path('signup/', views.signup, name='signup'),
        path('profile/password/', views.change_password, name='change_password'),
        path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]
