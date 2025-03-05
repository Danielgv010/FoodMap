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
    u.id AS restaurantId,
    u.name AS restaurantName,
    u.email,
    u.location,
    u.location_coordinates,
    CAST((SELECT
        CASE
            WHEN COUNT(r.rating) > 0 THEN AVG(CAST(r.rating AS DECIMAL(10,2)))
            ELSE 0  -- Or NULL if you want no reviews to be NULL
        END
    FROM main_review r
    WHERE r.restaurant_id = u.id
    ) AS FLOAT) AS averageRating,  -- Explicitly cast to FLOAT
    '{' +
    '"menus": "' + ISNULL((
        SELECT
            '[' + STUFF((
                SELECT
                    ',' +
                    '{' +
                    '"dish_name": "' + ISNULL(d.name, '') + '"' +
                    '}'
                FROM main_menu m
                JOIN main_dish d ON m.id = d.menu_id
                WHERE m.user_id = u.id
                FOR XML PATH('')
            ), 1, 1, '') + ']'
    ), '') + '",' +
    '"reviews": "' + ISNULL((
        SELECT
            '[' + STUFF((
                SELECT
                    ',' +
                    '{' +
                    '"content": "' + ISNULL(r.content, '') + '"' +
                    '}'
                FROM main_review r
                WHERE r.restaurant_id = u.id
                FOR XML PATH('')
            ), 1, 1, '') + ']'
    ), '') + '"' +
    '}' AS json_data
FROM main_user u
WHERE u.restaurant = 1;
""",
            reverse_sql="DROP VIEW IF EXISTS RestaurantIndexView;"
        ),
    ]