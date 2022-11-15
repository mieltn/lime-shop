from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Recipe, Ingredient, Basket
from .serializers import (
    CategorySerializer,
    RecipeSerializer,
    RecipeReadSerializer,
    IngredientSerializer,
    BasketSerializer,
    BasketReadSerializer
)


class CategoriesView(APIView):

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleCategoryView(APIView):

    def get(self, request, category_id):
        category = Category.objects.get(pk=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IngredientsView(APIView):

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipesView(APIView):

    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeReadSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipeDetails(APIView):

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BasketView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "to access basket user needs to login"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        basket = Basket.objects.get(pk=request.user.basket.id)
        serializer = BasketReadSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBasketView(APIView):

    def patch(self, request, ingredient_id):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "to access basket user needs to login"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        basket = Basket.objects.get(pk=request.user.basket.id)
        ingredient = Ingredient.objects.get(pk=ingredient_id)

        basket = basket.add_ingredient(ingredient)
        basket.total = basket.get_total()
        basket.save()

        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, ingredient_id):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "to access basket user needs to login"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        basket = Basket.objects.get(pk=request.user.basket.id)
        ingredient = Ingredient.objects.get(pk=ingredient_id)

        basket = basket.remove_ingredient(ingredient)
        basket.total = basket.get_total()
        basket.save()
        
        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClearBasketView(APIView):
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "to access basket user needs to login"},
                status = status.HTTP_401_UNAUTHORIZED
            )
        basket = Basket.objects.get(pk=request.user.basket.id)
        basket.ingredients.all().delete()
        basket.total = basket.get_total()
        basket.save()

        serializer = BasketSerializer(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)



