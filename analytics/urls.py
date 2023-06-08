from django.urls import path
from .views import *
from analytics import views
# from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path("index/",index),
    path("pichart/",pichart),
    path("payment/",payment),
    path("table/",table),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('data/', DataView.as_view(), name='data'),
]