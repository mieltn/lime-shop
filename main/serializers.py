from rest_framework import serializers
from .models import Category, Recipe, Ingredient, Basket
from .fields import CategoryRelatedField, IngredientRelatedField


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeSerializer(serializers.ModelSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all())
    ingredients = IngredientRelatedField(queryset=Ingredient.objects.all(), required=False)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'category', 'ingredients')
        

class RecipeReadSerializer(RecipeSerializer):
    category = serializers.StringRelatedField()
    ingredients = serializers.StringRelatedField(many=True)


class BasketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Basket
        fields = ('__all__')
