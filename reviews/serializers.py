from rest_framework import serializers
from main.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'content', 'restaurant']

    def create(self, validated_data, user):
        """
        Create and return a new `Review` instance, given the validated data.
        """
        validated_data['user'] = user  # Set the user from the request
        review = Review.objects.create(**validated_data)
        return review