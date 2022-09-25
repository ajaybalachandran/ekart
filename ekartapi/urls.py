from django.urls import path
from ekartapi import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('categories', views.CategoryView, basename='categories')
router.register('products', views.ProductsView, basename='products')
router.register("accounts/signup", views.UsersView, basename="users")
router.register('carts', views.CartsView, basename='carts')


urlpatterns = [

]+router.urls
