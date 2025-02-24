from django.shortcuts import render
from django.views.generic import TemplateView
from dotenv import load_dotenv
from FoodMap.settings import BASE_DIR

load_dotenv(dotenv_path=BASE_DIR / '.env')

class Home(TemplateView):
    template_name = 'main/home.html'