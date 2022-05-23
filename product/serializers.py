from rest_framework import serializers

from product.models import Category, NewProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewProduct
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
