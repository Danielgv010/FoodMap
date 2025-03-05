from django.urls import path
from . import views

urlpatterns = [
    path('api/search/', views.SearchAPIView.as_view(), name='search-api'),
]