from django.shortcuts import render
from django.views.generic import TemplateView
from dotenv import load_dotenv
from FoodMap.settings import BASE_DIR
from .models import Menu

load_dotenv(dotenv_path=BASE_DIR / '.env')

class Home(TemplateView):
    template_name = 'main/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Call the base implementation first
        menus = Menu.objects.all()  # Retrieve all menus (or apply filtering)
        context['menus'] = menus  # Add the menus to the context
        return context