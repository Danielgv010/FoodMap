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
                      SELECT json_group_array(
                        json_object(
                          'menu_id', m.id,
                          'set_menu', m.set_menu,
                          'menu_modified_date', m.modified_date,
                          'menu_price', m.price,
                          'Dishes', (
                            SELECT json_group_array(
                              json_object(
                                'dish_id', d.id,
                                'dish_name', d.name,
                                'dish_price', d.price,
                                'dish_promoted', d.promoted,
                                'dish_promotion_date', d.promotion_date,
                                'DishTypes', (
                                  SELECT json_group_array(
                                    json_object(
                                      'dish_type_id', dt.id,
                                      'dish_type', dt.type
                                    )
                                  )
                                  FROM main_dish_type_nm dtn
                                  JOIN main_dish_type dt ON dt.id = dtn.dish_type_id
                                  WHERE dtn.dish_id = d.id
                                )
                              )
                            )
                            FROM main_dish d
                            WHERE d.menu_id = m.id
                          )
                        )
                      )
                      FROM main_menu m
                      WHERE m.user_id = u.id
                    ) AS Menus,
                    (
                      SELECT json_group_array(
                        json_object(
                          'review_id', r.id,
                          'rating', r.rating,
                          'content', r.content,
                          'review_modified_date', r.modified_date,
                          'dish_id', r.dish_id
                        )
                      )
                      FROM main_review r
                      WHERE r.restaurant_id = u.id
                    ) AS Reviews
                FROM "main_user" u
                WHERE u.restaurant = 1;
            """,
            reverse_sql="DROP VIEW IF EXISTS RestaurantIndexView;"
        ),
    ]
