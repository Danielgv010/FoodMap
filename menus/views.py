from django.shortcuts import render
from django.views.generic import TemplateView
from main.models import User
from .utils import annotate_user_with_menu_existence


# Create your views here.

class ManageMenusView(TemplateView):
    template_name = 'menus/manage-menus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        user = annotate_user_with_menu_existence(User.objects.filter(pk=user.pk)).first()

        context['user'] = user

        return context