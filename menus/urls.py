from django.urls import path
from . import views

urlpatterns = [
    path('', views.ManageMenusView.as_view(), name='manage-menus'),
    path('add', views.AddMenuView.as_view(), name='add-menu'),
    path('api/menu/', views.AddMenuAPIView.as_view(), name='menu-api'),
]