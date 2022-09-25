from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet, ViewSet
from ekartapi.serializers import UserSerializer, CategorySerializer, ProductSerializer, CartSerializer, ReviewSerializer
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
        return Response(data=serializer.data)


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

    @action(methods=['POST'], detail=True)
    def add_to_cart(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        product = Products.objects.get(id=id)
        user = request.user
        serializer = CartSerializer(data=request.data, context={'product': product, 'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # localhost:8000/ekart/products/{pid}/add_review
    @action(methods=['POST'], detail=True)
    def add_review(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        product = Products.objects.get(id=id)
        serializer = ReviewSerializer(data=request.data, context={'product': product, 'user': request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

     # localhost:8000/ekart/products/{pid}/get_reviews
    @action(methods=['GET'], detail=True)
    def get_reviews(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        product = Products.objects.get(id=id)
        reviews = product.reviews_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)



class CartsView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Carts.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Carts.objects.filter(user=self.request.user)

    # def list(self, request, *args, **kwargs):
    #     user = request.user
    #     # cart = Carts.objects.filter(user=user)
    #     cart = user.carts_set.all()
    #     serializer = CartSerializer(cart, many=True)
    #     return Response(data=serializer.data)
