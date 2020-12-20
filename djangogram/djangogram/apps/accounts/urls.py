from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
        path('home/', views.home, name='home'),
        path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html')),
        path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html')),
        path('signup/', views.signup, name='signup'),
        path('profile/password/', views.change_password, name='change_password'),
        path('activate/<uidb64>/<token>/', views.activate, name='activate'),
        path('profile/', views.view_profile, name='view_profile'),
        path('profile/edit/', views.edit_profile, name='edit_profile'),
        path('profile/<username>/', views.profile_view, name='user_profile'),
        path('pictures/', views.profile_pictures, name='picture_list'),
        path('pictures/<username>/', views.pictures_view, name='user_pictures'),
        path('users/', views.profile_list, name='user_list'),
        path('edit/', views.edit_picture, name='edit_picture'),

]
