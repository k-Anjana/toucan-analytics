from django.urls import path
from .views import *

urlpatterns = [
    path("index/",index),
    path("pichart/",pichart),
    path("payment/",payment),
    path("table/",table),
   
  
]