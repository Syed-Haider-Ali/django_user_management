from django.urls import path
from user_auth.views import *

urlpatterns = [
    path('register', RegisterAPIView.as_view({"post": "create"})),
    path('login', LoginAPIView.as_view({"post": "login"})),
    path('logout', LogoutAPIView.as_view({"post": "logout"})),
    path('forget-password', ForgetPasswordAPIView.as_view({"post": "post"})),
    path('verify-otp', VerifyOtpAPIView.as_view({"post": "post"})),
    path('change-password', ChangePasswordAPIView.as_view({"post": "post"})),

]
