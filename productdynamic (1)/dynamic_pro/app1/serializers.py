# serializers.py

from rest_framework import serializers
from .models import Product, ProductVariant, Category, Attribute

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['id', 'name']

class ProductVariantSerializer(serializers.ModelSerializer):
    attributes = serializers.DictField(child=serializers.CharField()) 
    id = serializers.IntegerField(read_only=True) # Accept attributes as key-value pairs

    class Meta:
        model = ProductVariant
        fields = ['id','sku', 'price', 'stock', 'attributes']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes')
        variant = ProductVariant.objects.create(**validated_data)
        variant.attributes = attributes_data
        variant.save()
        return variant

class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True)

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'variants']

    def create(self, validated_data):
        variants_data = validated_data.pop('variants')
        product = Product.objects.create(**validated_data)
        
        # Create product variants
        for variant_data in variants_data:
            ProductVariant.objects.create(product=product, **variant_data)

        return product
