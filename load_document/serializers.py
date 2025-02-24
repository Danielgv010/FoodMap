# serializers.py
from rest_framework import serializers

class PDFUploadSerializer(serializers.Serializer):
    pdf_file = serializers.FileField()

    def validate_pdf_file(self, value):
        if value.content_type != 'application/pdf':
            raise serializers.ValidationError("The uploaded file must be a PDF.")
        if value.size > 4 * 1024 * 1024:  # 4MB limit
            raise serializers.ValidationError("File size exceeds 4MB.")
        return value
    
class TextToJsonSerializer(serializers.Serializer):
    string = serializers.CharField(
        required=True,
        allow_blank=False,
        max_length=10000
    )