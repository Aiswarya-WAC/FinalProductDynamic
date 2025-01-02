

from django.urls import path
from . import views

urlpatterns = [
    path('categories/', views.CategoryListCreate.as_view(), name='category-list-create'),
    path('attributes/', views.AttributeListCreate.as_view(), name='attribute-list-create'),
    path('products/', views.ProductListCreate.as_view(), name='product-list-create'),
    path('varientdetail/', views.ProductVariantDetail.as_view(), name='product-detail'),
    path('productdetail/', views.ProductDetailView.as_view(), name='product-detail'),  
]
