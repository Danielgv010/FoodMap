from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.db import IntegrityError
import requests
import os

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    location = serializers.CharField(max_length=255, required=False, allow_blank=True)

    def validate_password(self, value):
        return make_password(value)

    def create(self, validated_data):
        from main.models import User

        try:
            with transaction.atomic():
                location = validated_data.get('location', '')
                location_coordinates = None
                restaurant = True if location else False

                if location:
                    opencage_api_key = os.getenv('OPENCAGE_API_KEY')
                    if not opencage_api_key:
                        raise serializers.ValidationError({'error': 'OPENCAGE_API_KEY environment variable not set.'})

                    geocode_url = f"https://api.opencagedata.com/geocode/v1/json?q={location}&key={opencage_api_key}"
                    response = requests.get(geocode_url)
                    response.raise_for_status()
                    data = response.json()

                    if data and data['results']:
                        latitude = data['results'][0]['geometry']['lat']
                        longitude = data['results'][0]['geometry']['lng']
                        location_coordinates = f"{latitude},{longitude}"  # Store as string

                    else:
                        raise serializers.ValidationError({'location': 'Could not geocode the provided location.'})

                user = User.objects.create(
                    name=validated_data['name'],
                    email=validated_data['email'],
                    password=validated_data['password'],
                    location=location,
                    restaurant=restaurant,
                    location_coordinates=location_coordinates,
                )
                return user
        except IntegrityError as e:
            raise serializers.ValidationError({'email': 'This email address is already in use.'}) from e
        except requests.exceptions.RequestException as e:
            raise serializers.ValidationError({'error': f'Geocoding error: {str(e)}'}) from e
        except Exception as e:
            raise serializers.ValidationError({'error': str(e)}) from e
        
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(read_only=True)