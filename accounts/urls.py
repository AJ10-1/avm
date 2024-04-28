from django.urls import path
from .views import RegisterUser, LoginUser, Profile

urlpatterns = [
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
]
