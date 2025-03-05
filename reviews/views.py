from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from main.models import User
from .serializers import ReviewSerializer

class AddReviewAPIView(APIView):
    def post(self, request):
        user_id = request.session.get('user_id')  # Get user_id from session
        if not user_id:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = get_object_or_404(User, pk=user_id)  # Retrieve User object
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create(serializer.validated_data, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)