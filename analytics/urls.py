from django.urls import path
from .views import *

urlpatterns = [
    #path('analytics/',analytics),
    path('',index),
    path('emi/',emi),
    path('pie/',pie),
    path('payment/',payments),
    path('table/',table),
    
]