from django.urls import path
from .views import (
    CategoriesView,
    SingleCategoryView,
    RecipesView,
    RecipeDetails,
    BasketView,
    UpdateBasketView,
)

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:category_id>', SingleCategoryView.as_view()),

    path('recipes/', RecipesView.as_view()),
    path('recipes/<int:recipe_id>', RecipeDetails.as_view()),

    path('basket/', BasketView.as_view()),
    path('basket/<int:basket_id>', BasketView.as_view()),
    path('basket/<int:basket_id>/ingredients/<int:ingredient_id>', UpdateBasketView.as_view()),
]
