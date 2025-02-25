from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.hashers import make_password # for password hashing
from django.db import IntegrityError

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)  # write_only to not return password in response
    location = serializers.CharField(max_length=255, required=False, allow_blank=True) #location is optional


    def validate_password(self, value):
        """
        Hash the password before saving.  This is a MUST DO.
        """
        return make_password(value)  # Hash the password


    def create(self, validated_data):
        """
        Create and return a new `User` instance, given the validated data.  This is where you'd interact with your model.
        Important: You should not call Model.save() directly.
        """
        from main.models import User  #Import here to avoid circular import if the view is in the same file as the model.  Replace .models with the correct path if necessary.

        try:
            with transaction.atomic(): #Use transaction to handle errors during database operations
                location = validated_data.get('location', '')
                user = User.objects.create(
                    name=validated_data['name'],
                    email=validated_data['email'],
                    password=validated_data['password'], # Password already hashed in `validate_password`
                    location = location,
                    restaurant = True if location else False #Restaurant is false if location exists.
                )
                return user
        except IntegrityError as e: # Catch unique constraint errors (e.g., duplicate email)
            raise serializers.ValidationError({'email': 'This email address is already in use.'}) from e
        except Exception as e: #Catch all other errors
            raise serializers.ValidationError({'error': str(e)}) from e