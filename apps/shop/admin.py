from django.contrib import admin

from .models import Category, Review, Product


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
