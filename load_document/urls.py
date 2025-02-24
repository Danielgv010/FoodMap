from django.urls import path
from .views import OCRFileUploadView, TextToJsonView, PdfOcrToJsonView

urlpatterns = [
    path('upload-pdf/', OCRFileUploadView.as_view(), name='upload-pdf'),
    path('text-to-json/', TextToJsonView.as_view(), name='text-to-json'),
    path('pdf_ocr_to_json/', PdfOcrToJsonView.as_view(), name='pdf_ocr_to_json'),
]