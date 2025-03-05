# yourapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from django.conf import settings
from django.shortcuts import render
from main.models import Menu, User  # Import your Menu and User models (adjust import path if needed)
from django.template.loader import render_to_string

class SearchAPIView(APIView):
    def get(self, request):
        search_string = request.query_params.get('search', None)
        if not search_string:
            return Response({"error": "Search string is required."}, status=status.HTTP_400_BAD_REQUEST)

        endpoint = settings.AZURE_SEARCH_ENDPOINT
        index_name = settings.AZURE_SEARCH_INDEX_NAME
        api_key = settings.AZURE_SEARCH_API_KEY

        search_client = SearchClient(endpoint=endpoint,
                                     index_name=index_name,
                                     credential=AzureKeyCredential(api_key))

        try:
            results = search_client.search(search_string)

            # Extract restaurant IDs from Azure AI Search results
            restaurant_ids = []
            for result in results:
                try:
                    restaurant_id = result.get("restaurantId")  # Changed to restaurantId
                    restaurant_ids.append(restaurant_id)
                except Exception as e:
                    print(f"error getting restaurant id: {e}")
                    continue

            print(f"Azure AI Search restaurant_ids: {restaurant_ids}")

            # Fetch Menu objects from the database based on the restaurant IDs
            # First, try filtering directly (most efficient):
            try:
                menus = Menu.objects.filter(user_id__in=restaurant_ids)
                print(f"Menus found using user_id__in: {menus}")
            except Exception as e:
                print(f"Error with user_id__in filter: {e}")
                menus = [] # set to empty in case it fails to avoid type errors with if statement below


            # ALTERNATIVE APPROACH: If direct filtering isn't working (due to potential type issues)
            # This is less efficient, but more robust if there are type mismatches
            if not menus:  # If the first query failed or returned empty
                print("Attempting alternative menu fetch method...")
                menus = []
                for restaurant_id in restaurant_ids:
                    try:
                        menu = Menu.objects.filter(user_id=restaurant_id) # Fetch menu with restaurant id
                        if (menu): # if menu exists
                            menus.append(menu[0]) # there will only be 1 menu, append the first object.
                    except Exception as e:
                        print(f"Error fetching menu for restaurant_id {restaurant_id}: {e}")

             # Render the menus to a string using the same template snippet
            rendered_menus = render_to_string('main/partials/menu_list.html', {'menus': menus})

            # Return the rendered HTML
            return Response({'menus_html': rendered_menus}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error during search: {e}")
            return Response({"error": "Search failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)