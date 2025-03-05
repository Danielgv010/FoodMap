from django.urls import path
from . import views

urlpatterns = [
    path('api/add-review/', views.AddReviewAPIView.as_view(), name='add-review-api'),
]