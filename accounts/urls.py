from django.urls import path
from . import views

urlpatterns = [
    path('register-form/', views.RegisterView.as_view(), name='register'),
    path('register/', views.RegisterAPIView.as_view(), name='register-submit'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
]