# models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Attribute(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name='variants', on_delete=models.CASCADE)
    sku = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    attributes = models.JSONField()  # Store attributes as key-value pairs

    def __str__(self):
        return f'{self.product.name} - {self.sku}'
