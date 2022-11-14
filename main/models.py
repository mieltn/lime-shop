from django.db import models


class Category(models.Model):
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
    ingredients = models.ManyToManyField(Ingredient, null=True)

    def __str__(self):
        return self.name


class Basket(models.Model):
    ingredients = models.ManyToManyField(Ingredient)

    def __str__(self):
        return self.ingredients

