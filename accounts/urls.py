from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path("profile/", views.profile, name="profile"),
    path(
    "profile/edit/",
    views.edit_profile,
    name="edit_profile"
),
path(
    "change-password/",
    auth_views.PasswordChangeView.as_view(
        template_name="accounts/change_password.html"
    ),
    name="change_password",
),
]