from django.db import models


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
    price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=1024)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    ingredients = models.ManyToManyField(Ingredient)
    cuisine = models.ForeignKey(Cuisine, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Basket(models.Model):
    ingredients = models.ManyToManyField(Ingredient)
    total = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    def add_ingredient(self, ingredient):
        self.ingredients.add(ingredient)
        return self

    def remove_ingredient(self, ingredient):
        self.ingredients.remove(ingredient)
        return self

    def get_total(self):
        return sum([ingredient.price for ingredient in self.ingredients.all()])

    def clear_basket(self):
        for ingredient in self.ingredients.all():
            self.remove_ingredient(ingredient)

