from rest_framework import serializers
from django.contrib.auth.models import User
from ekartapi.models import Category, Products, Carts


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Category
        fields = ['category_name', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'

    def create(self, validated_data):
        category = self.context.get('category')
        return Products.objects.create(**validated_data, category=category)


class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    product = serializers.CharField(read_only=True)
    created_date = serializers.CharField(read_only=True)
    status = serializers.CharField(read_only=True)
    class Meta:
        models = Carts
        fields = '__all__'

