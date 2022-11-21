from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from limeshop.permissions import IsAuthAdminOrReadOnly
from .models import Category, Cuisine, Recipe, Ingredient, Basket
from .serializers import (
    CategorySerializer,
    CuisineSerializer,
    RecipeSerializer,
    RecipeReadSerializer,
    IngredientSerializer,
    # ItemSerializer,
    BasketSerializer,
    # BasketReadSerializer
)
from . import utils


class CategoriesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthAdminOrReadOnly]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "authentication is required for this action"}
            )
        if not request.user.is_admin:
            return Response(
                {"msg": "admin access is required for this action"}
            )
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuisineView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        cuisine = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "authentication is required for this action"}
            )
        if not request.user.is_admin:
            return Response(
                {"msg": "admin access is required for this action"}
            )
        serializer = CuisineSerializer(data=request.data)
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
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "authentication is required for this action"}
            )
        if not request.user.is_admin:
            return Response(
                {"msg": "admin access is required for this action"}
            )
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RecipesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthAdminOrReadOnly]

    def get(self, request):
        categories = utils.set_filter(request, Category, 'category')
        cuisine = utils.set_filter(request, Cuisine, 'cuisine')
        # cooking_time = utils.set_filter(request, )
        ingredients = utils.set_filter(request, Ingredient, 'ingredient')
        
        recipes = (
            Recipe.objects
            .filter(
                category__in=categories,
                ingredients__in=ingredients,
                cuisine__in=cuisine)
            .distinct()
            .all()
        )

        serializer = RecipeReadSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"msg": "authentication is required for this action"}
            )
        if not request.user.is_admin:
            return Response(
                {"msg": "admin access is required for this action"}
            )
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def get(self, request):
    #     basket = Basket.objects.get(pk=request.user.basket.id)
    #     serializer = BasketReadSerializer(basket)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def patch(self, request):
    #     basket = Basket.objects.get(pk=request.user.basket.id)
    #     ingredient = Ingredient.objects.get(name=request.data['name'])

    #     basket = basket.add_ingredient(ingredient)
    #     basket.total = basket.get_total()
    #     basket.save()

    #     serializer = BasketSerializer(basket)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def delete(self, request):
    #     basket = Basket.objects.get(pk=request.user.basket.id)
    #     ingredient = Ingredient.objects.get(name=request.data['name'])

    #     basket = basket.remove_ingredient(ingredient)
    #     basket.total = basket.get_total()
    #     basket.save()
        
    #     serializer = BasketSerializer(basket)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    def get(self, request):
        basket = utils.calculate_basket(request.user.id)
        return Response(basket, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['user'] = request.user.id
        serializer = BasketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            basket = utils.calculate_basket(request.user.id)
            return Response(basket, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        ingredient = Ingredient.objects.get(name=request.data.get('ingredient'))
        item = Basket.objects.filter(user=request.user, ingredient=ingredient).first()
        item.delete()
        basket = utils.calculate_basket(request.user.id)
        return Response(basket, status=status.HTTP_200_OK)


class ClearBasketView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        items = Basket.objects.filter(user=request.user)
        items.delete()
        return Response(
            {"msg": "successfully cleared the basket"},
            status=status.HTTP_200_OK
        )



# class ClearBasketView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def delete(self, request):
#         basket = Basket.objects.get(pk=request.user.basket.id)
#         basket.clear_basket()
#         basket.total = basket.get_total()
#         basket.save()
#         serializer = BasketSerializer(basket)
#         return Response(serializer.data, status=status.HTTP_200_OK)



