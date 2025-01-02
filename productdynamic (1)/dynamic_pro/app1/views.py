from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Attribute, Product, ProductVariant
from .serializers import CategorySerializer, AttributeSerializer, ProductSerializer, ProductVariantSerializer

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size' 
    max_page_size = 100  

class CategoryListCreate(APIView):
    def get(self, request):
        categories = Category.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_categories = paginator.paginate_queryset(categories, request)
        serializer = CategorySerializer(paginated_categories, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AttributeListCreate(APIView):
    def get(self, request):
        attributes = Attribute.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_attributes = paginator.paginate_queryset(attributes, request)
        serializer = AttributeSerializer(paginated_attributes, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductListCreate(APIView):
    def get(self, request):
        products = Product.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductVariantDetail(APIView):
    def get(self, request, *args, **kwargs):
        variant_id = request.query_params.get('id')
        sku = request.query_params.get('sku')

        if not variant_id and not sku:
            return Response({"error": "Please provide either 'id' or 'sku' as query parameters."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch the product variant based on 'id' or 'sku'
        variant = None
        if variant_id:
            variant = ProductVariant.objects.filter(id=variant_id).first()
        elif sku:
            variant = ProductVariant.objects.filter(sku=sku).first()

        if not variant:
            return Response({"error": "Product variant not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the variant data
        variant_serializer = ProductVariantSerializer(variant)
        return Response(variant_serializer.data, status=status.HTTP_200_OK)
       
class ProductDetailView(APIView):
    def get(self, request, *args, **kwargs):
        # Get 'id' from query parameters
        product_id = request.query_params.get('id')

        if not product_id:
            return Response({"error": "Please provide 'id' as a query parameter."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Fetch the product by ID
        product = Product.objects.filter(id=product_id).first()

        if not product:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Serialize and return the product data
        product_serializer = ProductSerializer(product)
        return Response(product_serializer.data, status=status.HTTP_200_OK)
