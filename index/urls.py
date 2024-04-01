from django.urls import path
from . import views
from .views import (
    CartList, CartDetail, 
    WishlistList, WishlistDetail,
    ProductList, ProductDetail,
    CategoryList, CategoryDetail,
    SubcategoryList, SubcategoryDetail,SizeList,SizeDetail,
    BrandList,BrandDetail
)

urlpatterns = [
    path('', views.index, name='index'),
    # Cart URLs
    path('cart/', CartList.as_view(), name='cart-list'),
    path('cart/<int:pk>/', CartDetail.as_view(), name='cart-detail'),
    # path('checkout/', Checkout.as_view(), name='checkout'),

    # Wishlist URLs
    path('wishlist/', WishlistList.as_view(), name='wishlist-list'),
    path('wishlist/<int:pk>/', WishlistDetail.as_view(), name='wishlist-detail'),

    # Size URLs
    path('size/', SizeList.as_view(), name='size-list'),
    path('size/<int:pk>/', SizeDetail.as_view(), name='size-detail'),

    # Brand Urls
    path('brand/', BrandList.as_view(), name='brand-list'),
    path('brand/<int:pk>/', BrandDetail.as_view(), name='brand-detail'),
    
    # Product URLs
    path('product/', ProductList.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetail.as_view(), name='product-detail'),

    # Category URLs
    path('category/', CategoryList.as_view(), name='category-list'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),

    # Subcategory URLs
    path('subcategory/', SubcategoryList.as_view(), name='subcategory-list'),
    path('subcategory/<int:pk>/', SubcategoryDetail.as_view(), name='subcategory-detail'),
]