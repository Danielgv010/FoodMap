from rest_framework import serializers
from django.db import transaction
from main.models import Menu, Dish
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class MenuSerializer(serializers.Serializer):
    menu_price = serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True)
    set_menu = serializers.BooleanField()
    dish_name = serializers.ListField(child=serializers.CharField(max_length=100, allow_blank=True, required=False), allow_empty=True, required=False)
    dish_price = serializers.ListField(child=serializers.DecimalField(max_digits=6, decimal_places=2, required=False, allow_null=True), allow_empty=True, required=False)
    dish_promoted = serializers.ListField(child=serializers.BooleanField(), allow_empty=True, required=False)

    def create(self, validated_data, user):
        with transaction.atomic():
            try:
                menu = Menu.objects.create(
                    user=user,
                    set_menu=validated_data['set_menu'],
                    price=validated_data.get('menu_price')  # Use .get to handle potential None
                )

                dish_names = validated_data.get('dish_name', [])
                dish_prices = validated_data.get('dish_price', [])
                dish_promoted = validated_data.get('dish_promoted', [])

                # Get the minimum length of the dish lists to avoid IndexErrors
                num_dishes = min(len(dish_names), len(dish_prices), len(dish_promoted))

                # Ensure all dish lists have the same length
                for i in range(num_dishes):
                    Dish.objects.create(
                        menu=menu,
                        name=dish_names[i] if i < len(dish_names) else '',
                        price=dish_prices[i] if i < len(dish_prices) else None,
                        promoted=dish_promoted[i] if i < len(dish_promoted) else False,
                        promotion_date=timezone.now()  # Or handle this differently based on your requirements
                    )

                return menu
            except Exception as e:
                logger.exception("Error creating menu and dishes: %s", e)  # Log the full exception
                raise  # Re-raise the exception so it's caught by the API view