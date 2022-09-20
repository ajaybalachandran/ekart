from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet, ViewSet
from ekartapi.serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer
from rest_framework import permissions
from ekartapi.models import Category, Products, Carts
from rest_framework.response import Response
from rest_framework.decorators import action


class UsersView(ViewSet):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class CategoryView(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAdminUser]

    @action(methods=["POST"], detail=True)
    def add_product(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        cat = Category.objects.get(id=id)
        serializer = ProductSerializer(data=request.data, context={"category":cat})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    @action(methods=["GET"], detail=True)
    def products(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        cat = Category.objects.get(id=id)
        products = cat.products_set.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductsView(ViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        all_products = Products.objects.all()
        serializer = ProductSerializer(all_products, many=True)
        return Response(data=serializer.data)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        product = Products.objects.get(id=id)
        serializer = ProductSerializer(product,many=False)
        return Response(data=serializer.data)


class CartsView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()

    def create(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        pro = Products.objects.get(id=id)
        user = request.user
        Carts.objects.create(user=user, product=pro)
        return Response(data='created')

