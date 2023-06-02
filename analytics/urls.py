from django.urls import path
from .views import *
from analytics import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("index/",index),
    path("pichart/",pichart),
    path("payment/",payment),
    path("table/",table),
]