from django.urls import path
from . import views


urlpatterns = [
    path("login/", views.LoginUser.as_view(), name="Login route"),
    path("<int:pk>/", views.UserDetails.as_view(), name="details"),
    path("v1/users/", views.UserList.as_view(), name="All user routes"),
    path("v1/register/", views.RegisterUser.as_view(), name="Signup route"),
]