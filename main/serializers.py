from rest_framework import serializers
from .models import Category, Cuisine, Recipe, Ingredient, Basket
from .fields import CategoryRelatedField, IngredientRelatedField, CuisineRelatedField
from limeshop.settings import STATIC_URL


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

    # image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Ingredient
        fields = ('__all__')

    # def get_image_url(self, instance):
    #     if instance.image.url:
    #         return instance.image.url
    #     return


class RecipeSerializer(ImageSerializer):
    category = CategoryRelatedField(queryset=Category.objects.all())
    cuisine = CuisineRelatedField(queryset=Cuisine.objects.all())
    ingredients = IngredientRelatedField(queryset=Ingredient.objects.all(), required=False)
    # image = serializers.SerializerMethodField('get_image_url')

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'category', 'cuisine', 'ingredients', 'image')

    # def get_image_url(self, instance):
    #     if instance.image:
    #         return instance.image.url
    #     return
        

class RecipeReadSerializer(RecipeSerializer):
    category = serializers.StringRelatedField()
    cuisine = serializers.StringRelatedField()
    ingredients = serializers.StringRelatedField(many=True)


class BasketSerializer(serializers.ModelSerializer):

    ingredient = IngredientRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = Basket
        fields = ('ingredient', 'user')
