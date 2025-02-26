from django.urls import path
from . import views

urlpatterns = [
    path('', views.RegisterView.as_view(), name='register'),
    path('register/', views.RegisterAPIView.as_view(), name='register-submit'),
]