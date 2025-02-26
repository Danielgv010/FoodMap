from django.views.generic import TemplateView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import serializers
from .serializers import LogoutSerializer, RegisterSerializer, LoginSerializer
from django.contrib.auth.hashers import check_password
from main.models import User
from django.contrib.auth import logout as django_logout

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

class LoginAPIView(APIView):
    @extend_schema(
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(response={"type": "object", "properties": {"token": {"type": "string"}}}, description="Login successful"),
        400: OpenApiResponse(description="Invalid credentials"),
    }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):  # Validate serializer
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            if check_password(password, user.password): # Verify hashed password

                # Use session based authentication - You can skip token generation
                request.session['user_id'] = user.id # store user_id in session - important

                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK) #Modify as needed.

            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    serializer_class = LogoutSerializer # add the serializer
    def post(self, request):
        django_logout(request)  # removes user_id from session
        return Response(status=status.HTTP_204_NO_CONTENT)