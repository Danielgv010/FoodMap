from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageMenusView.as_view(), name='manage-menus'),
]