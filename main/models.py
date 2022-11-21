from django.db import models
from users.models import User
from limeshop.settings import STATIC_URL


class Category(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Cuisine(models.Model):
    name = models.CharField(max_length=128)
    
    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    image = models.ImageField(upload_to=STATIC_URL + 'images/ingredients/', null=True, blank=True)


    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(upload_to=STATIC_URL + 'images/recipes/', null=True, blank=True)

    def __str__(self):
        return self.name


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)

    def __str__(self):
        return self.ingredient.name


class Review(models.Model):
    title = models.CharField(max_length=128)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.DecimalField(decimal_places=1, max_digits=2)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.title


