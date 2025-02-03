from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('otp_verify_signup/', views.otp_verify_signup, name='otp_verify_signup'),
    path('signin/', views.signin, name='signin'),
    path('otp_verify_signin/', views.otp_verify_signin, name='otp_verify_signin'),
    path('signout/', views.signout, name='signout'),
]