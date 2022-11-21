from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from limeshop.permissions import IsAuthAdminOrReadOnly
from .models import (
    Category,
    Cuisine,
    Recipe,
    Ingredient,
    Basket,
    Review,
)
from .serializers import (
    CategorySerializer,
    CuisineSerializer,
    RecipeSerializer,
    RecipeReadSerializer,
    IngredientSerializer,
    BasketSerializer,
    ReviewSerializer,
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
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CuisineView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthAdminOrReadOnly]

    def get(self, request):
        cuisine = Cuisine.objects.all()
        serializer = CuisineSerializer(cuisine, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
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
    permission_classes = [IsAuthAdminOrReadOnly]

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
            {"detail": "Successfully cleared the basket"},
            status=status.HTTP_200_OK
        )


class ReviewsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, recipe_id):
        reviews = Review.objects.filter(recipe_id=recipe_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, recipe_id):
        request.data['user'] = request.user.id
        request.data['recipe'] = recipe_id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)