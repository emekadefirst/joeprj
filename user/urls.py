from django.urls import path
from . import views


urlpatterns = [
    path("v1/login/", views.LoginUser.as_view(), name="Login route"),
    path("<int:pk>/", views.UserDetails.as_view(), name="details"),
    path("v1/users/", views.UserList.as_view(), name="All user routes"),
    path("v1/register/", views.RegisterUser.as_view(), name="Signup route"),
    path("v1/request-reset/", views.RequestPasswordReset.as_view(), name="request-reset"),
    path("v1/verify-otp/", views.VerifyOTP.as_view(), name="verify-otp"),
    path("v1/reset-password/", views.ResetPassword.as_view(), name="reset-password"),
]