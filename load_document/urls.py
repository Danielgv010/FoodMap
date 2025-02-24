from django.urls import path
from .views import OCRFileUploadView, TextToJsonView, OcrToJsonView

urlpatterns = [
    path('ocr-upload/', OCRFileUploadView.as_view(), name='ocr-upload'),
    path('text-to-json/', TextToJsonView.as_view(), name='text-to-json'),
    path('ocr-to-json/', OcrToJsonView.as_view(), name='ocr-to-json'),
]