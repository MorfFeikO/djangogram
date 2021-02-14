from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


app_name = 'accounts'
urlpatterns = [
        path('', views.home, name='home'),
        path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
        path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
        path('signup/', views.signup, name='signup'),
        path('profile/password/', views.change_password, name='change_password'),
        path('activate/<uidb64>/<token>/', views.activate, name='activate'),
        path('profile/edit/', views.edit_profile, name='edit_profile'),

        path('profile_page/', views.new_profile_view, name='profile_page'),
        path('profile_page/<str:pk>/', views.new_profile_view, name='profile_page_friend'),
        path('profile_page/<str:pk>/<str:operation>/', views.operation_with_friends, name='operation'),
        path('profile_page/<str:pk>/<str:operation>/<int:picture_id>/', views.operation_with_friends, name='like'),

]
