from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    restaurant = models.BooleanField()
    location = models.CharField(max_length=100, null=True, blank=True)
    location_coordinates = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')  # Use db_column to specify the column name
    set_menu = models.BooleanField()
    modified_date = models.DateTimeField(auto_now=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"Menu for {self.user.name} {'(Set)' if self.set_menu else '(A la Carte)'}"

    
class Dish(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, db_column='menu_id')  # Specify the column name to avoid duplication
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    promoted = models.BooleanField(null=True, blank=True)
    promotion_date = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - ${self.price}"
    
class Dish_Type(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100)
    
    def __str__(self):
        return self.type
    
class Dish_Type_NM(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, db_column='dish_id')  # Fix the column name
    dish_type = models.ForeignKey(Dish_Type, on_delete=models.CASCADE, db_column='dish_type_id')  # Fix the column name

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews', db_column='user_id')  # Fix column name
    restaurant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='restaurant_reviews', db_column='restaurant_id')  # Fix column name
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, null=True, blank=True, db_column='dish_id')  # Fix column name
    rating = models.IntegerField()
    content = models.TextField()
    modified_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Review by {self.user.name} for {self.dish.name if self.dish else 'Restaurant'}"
