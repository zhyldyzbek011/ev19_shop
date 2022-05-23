from django.contrib import admin
from product.models import Category, NewProduct, Product

admin.site.register(Product)
admin.site.register(NewProduct)
admin.site.register(Category)
