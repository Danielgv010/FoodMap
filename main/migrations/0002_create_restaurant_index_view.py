from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                    CREATE VIEW RestaurantIndexView AS
    SELECT
        u.id AS user_id,
        u.name AS user_name,
        u.email,
        u.location,
        u.location_coordinates,
        (
            SELECT
                STUFF((
                    SELECT ',' +
                        '<Menu>' +
                            '<menu_id>' + CAST(m.id AS VARCHAR(10)) + '</menu_id>' +
                            '<set_menu>' + CAST(m.set_menu AS VARCHAR(5)) + '</set_menu>' +
                            '<menu_modified_date>' + CONVERT(VARCHAR, m.modified_date, 120) + '</menu_modified_date>' +
                            '<menu_price>' + ISNULL(CAST(m.price AS VARCHAR(20)), '') + '</menu_price>' +
                            '<Dishes>' +
                                (SELECT
                                    STUFF((
                                        SELECT ',' +
                                            '<Dish>' +
                                                '<dish_id>' + CAST(d.id AS VARCHAR(10)) + '</dish_id>' +
                                                '<dish_name>' + ISNULL(d.name, '') + '</dish_name>' +
                                                '<dish_price>' + ISNULL(CAST(d.price AS VARCHAR(20)), '') + '</dish_price>' +
                                                '<dish_promoted>' + ISNULL(CAST(d.promoted AS VARCHAR(5)), '') + '</dish_promoted>' +
                                                '<dish_promotion_date>' + ISNULL(CONVERT(VARCHAR, d.promotion_date, 120), '') + '</dish_promotion_date>' +
                                                '<DishTypes>' +
                                                    (SELECT
                                                        STUFF((
                                                            SELECT ',' +
                                                                '<DishType>' +
                                                                    '<dish_type_id>' + CAST(dt.id AS VARCHAR(10)) + '</dish_type_id>' +
                                                                    '<dish_type>' + ISNULL(dt.type, '') + '</dish_type>' +
                                                                '</DishType>'
                                                            FROM main_dish_type_nm dtn
                                                            JOIN main_dish_type dt ON dt.id = dtn.dish_type_id
                                                            WHERE dtn.dish_id = d.id
                                                            FOR XML PATH(''), TYPE
                                                        ).value('.', 'VARCHAR(MAX)'), 1, 1, '')
                                                    ) +
                                                '</DishTypes>' +
                                            '</Dish>'
                                        FROM main_dish d
                                        WHERE d.menu_id = m.id
                                        FOR XML PATH(''), TYPE
                                    ).value('.', 'VARCHAR(MAX)'), 1, 1, '')
                                ) +
                            '</Dishes>' +
                        '</Menu>'
                    FROM main_menu m
                    WHERE m.user_id = u.id
                    FOR XML PATH(''), TYPE
                ).value('.', 'VARCHAR(MAX)'), 1, 1, '')
        ) AS Menus,
        (
            SELECT
                STUFF((
                    SELECT ',' +
                        '<Review>' +
                            '<review_id>' + CAST(r.id AS VARCHAR(10)) + '</review_id>' +
                            '<rating>' + CAST(r.rating AS VARCHAR(3)) + '</rating>' +
                            '<content>' + ISNULL(r.content, '') + '</content>' +
                            '<review_modified_date>' + CONVERT(VARCHAR, r.modified_date, 120) + '</review_modified_date>' +
                            '<dish_id>' + ISNULL(CAST(r.dish_id AS VARCHAR(10)), '') + '</dish_id>' +
                        '</Review>'
                    FROM main_review r
                    WHERE r.restaurant_id = u.id
                    FOR XML PATH(''), TYPE
                ).value('.', 'VARCHAR(MAX)'), 1, 1, '')
        ) AS Reviews
    FROM main_user u
    WHERE u.restaurant = 1;
            """,
            reverse_sql="DROP VIEW IF EXISTS RestaurantIndexView;"
        ),
    ]