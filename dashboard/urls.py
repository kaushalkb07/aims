from django.urls import path
from .import views

 # URL for signup
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
 ]