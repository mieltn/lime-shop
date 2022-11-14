from django.contrib import admin
from .models import Category, Recipe, Ingredient, Basket

# Register your models here.
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Basket)
