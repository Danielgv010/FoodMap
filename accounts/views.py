from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from .serializers import RegisterSerializer

class RegisterView(TemplateView):
    template_name = 'accounts/register.html'

class RegisterAPIView(APIView):
    parser_classes = (MultiPartParser,)  #Accepts form data

    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: OpenApiResponse(response={"type": "object", "properties": {"message": {"type": "string"}}}, description="Registration successful"),
            400: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Validation error"),
            500: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}}, description="Server error"),
        },
    )
    def post(self, request):
        try:
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.create(serializer.validated_data)
                return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)