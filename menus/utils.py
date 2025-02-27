def annotate_user_with_menu_existence(queryset):
    from django.db.models import Exists, OuterRef, BooleanField
    from main.models import Menu

    queryset = queryset.annotate(
        has_menus=Exists(
            Menu.objects.filter(user=OuterRef('pk')),
            output_field=BooleanField()
        )
    )
    return queryset