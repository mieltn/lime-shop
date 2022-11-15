from django.urls import path
from .views import (
    UserView,
    LoginUser,
    LogoutUser,
)
urlpatterns = [
    path('user/', UserView.as_view()),
    path('login/', LoginUser.as_view()),
    path('logout/', LogoutUser.as_view()),
]