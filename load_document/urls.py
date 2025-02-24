from django.urls import path
from .views import OCRFileUploadView, TextToJsonView, OcrToJsonView

urlpatterns = [
    path('upload-pdf/', OCRFileUploadView.as_view(), name='upload-pdf'),
    path('text-to-json/', TextToJsonView.as_view(), name='text-to-json'),
    path('ocr_to_json/', OcrToJsonView.as_view(), name='ocr_to_json'),
]