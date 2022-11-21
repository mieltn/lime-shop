from django.urls import path
from .views import (
    CategoriesView,
    CuisineView,
    SingleCategoryView,
    IngredientsView,
    RecipesView,
    RecipeDetails,
    BasketView,
    ClearBasketView,
    ReviewsView,
)

urlpatterns = [
    path('categories/', CategoriesView.as_view()),
    path('categories/<int:category_id>', SingleCategoryView.as_view()),

    path('cuisine/', CuisineView.as_view()),

    path('ingredients/', IngredientsView.as_view()),

    path('recipes/', RecipesView.as_view()),
    path('recipes/<int:recipe_id>', RecipeDetails.as_view()),

    path('basket/', BasketView.as_view()),
    path('basket/ingredients/', BasketView.as_view()),
    path('basket/checkout/', ClearBasketView.as_view()),

    path('recipes/<int:recipe_id>/reviews/', ReviewsView.as_view()),
]
