from rest_framework import serializers
from .models import Category, Cuisine, Recipe, Ingredient, Basket, Review
from .fields import CategoryRelatedField, IngredientRelatedField, CuisineRelatedField
from limeshop.settings import STATIC_URL

from statistics import mean


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('__all__')


class CuisineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cuisine
        fields = ('__all__')


class ImageSerializer(serializers.ModelSerializer):

    image = serializers.SerializerMethodField('get_image_url')

    def get_image_url(self, instance):
        if instance.image:
            return instance.image.url
        return


class IngredientSerializer(ImageSerializer):

    class Meta:
        model = Ingredient
        fields = ('__all__')


class RecipeSerializer(ImageSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all())
    cuisine = CuisineRelatedField(queryset=Cuisine.objects.all())
    ingredients = IngredientRelatedField(queryset=Ingredient.objects.all(), required=False)

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'category', 'cuisine', 'ingredients', 'image', 'reviews')
        

class RecipeReadSerializer(RecipeSerializer):
    category = serializers.StringRelatedField()
    cuisine = serializers.StringRelatedField()
    ingredients = serializers.StringRelatedField(many=True)
    reviews = serializers.SerializerMethodField('calculate_rate')

    def calculate_rate(self, instance):
        if instance.review_set.all():
            return round(mean([
                review.rate
                for review
                in instance.review_set.all()
            ]), 1)
        return


class BasketSerializer(serializers.ModelSerializer):

    ingredient = IngredientRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = Basket
        fields = ('ingredient', 'user')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('__all__')
