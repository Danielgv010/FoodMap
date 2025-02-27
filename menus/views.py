from django.urls import reverse
from django.views.generic import TemplateView
from main.models import User, Menu
from .utils import annotate_user_with_menu_existence
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import MenuSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse
import logging

from .serializers import MenuSerializer  # Import the serializer
from main.models import User  # Ensure you're importing your custom User model

logger = logging.getLogger(__name__)
# Create your views here.

class ManageMenusView(TemplateView):
    template_name = 'menus/manage-menus.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_id = self.request.session.get('user_id')  # Get user_id from session

        if not user_id:
            # User not authenticated. Redirect to login or show an error
            login_url = reverse('login')  # Replace 'login' with your actual login URL name
            return redirect(login_url) #This will stop to execute this function

        user = get_object_or_404(User, pk=user_id)  # Retrieve User object by ID

        user = annotate_user_with_menu_existence(User.objects.filter(pk=user.pk)).first()

        menus = Menu.objects.filter(user=user)

        context['user'] = user
        context['menus'] = menus

        return context
    

class AddMenuView(View):
    def get(self, request):
        return render(request, 'menus/add-menu.html')

    def post(self, request):
        return render(request, 'menus/add-menu.html')
    

class AddMenuAPIView(APIView):
    parser_classes = (JSONParser, MultiPartParser, FormParser) #Now set JSONParser

    @extend_schema(
        request=MenuSerializer,
        responses={
            201: OpenApiResponse(response={"type": "object", "properties": {"message": {"type": "string"}}},
                                  description="Menu created successfully"),
            400: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}},
                                  description="Validation error"),
            500: OpenApiResponse(response={"type": "object", "properties": {"error": {"type": "string"}}},
                                  description="Server error"),
        },
    )
    def post(self, request):
        logger.debug("MenuAPIView - request.session.items(): %s", request.session.items())
        try:
            user_id = request.session.get('user_id')  # Get user_id from session

            if not user_id:
                return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

            user = get_object_or_404(User, pk=user_id)  # Retrieve User object
            try:

                serializer = MenuSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                    logger.debug("MenuAPIView - Serializer validated data: %s", serializer.validated_data)
                    menu = serializer.create(serializer.validated_data, user)  # Pass the user
                    return Response({"message": "Menu created successfully", "menu_id": menu.id},
                                    status=status.HTTP_201_CREATED)
                else:
                    logger.error("MenuAPIView - Serializer errors: %s", serializer.errors)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except serializers.ValidationError as e:
                logger.error("MenuAPIView - Validation Error: %s", e.detail)
                return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.exception("MenuAPIView - Exception: %s", e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)