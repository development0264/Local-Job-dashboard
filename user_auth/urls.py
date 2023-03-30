import imp
from django.contrib import admin
from django.urls import path, include
from user_auth.views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login', csrf_exempt(UserLogin.as_view()), name='login'),
    # path('mapdetails/', MapDetails.as_view(), name='mapdetails'),
    path('userprofile',  csrf_exempt(UserProfileView.as_view()), name='userprofile'),
    path('change_password/<int:pk>', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('logout', LogoutView, name='auth_logout')
    path('logout', LogoutView.as_view(), name='auth_logout'),

    path('api/service_provider', service_provider,name="bids_list"),
    # path('changepassword/', UserChangePassword.as_view(), name='changepassword'),
    # path('send-reset-password-email/', SendPasswordResetEmail.as_view(),
    #  name='send-reset-password-email'),
    # path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(),
    #  name='reset-password/'),
]



