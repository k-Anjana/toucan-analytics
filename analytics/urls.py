from django import views
from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    #path('analytics/',analytics),
    path('',index),
    path('emi/',emi),
    path('pie/',pie),
    path('payment/',payments),
    path('table/',table),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('hello/', HelloView.as_view(), name='hello'),
]