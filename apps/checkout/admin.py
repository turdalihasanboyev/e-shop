from django.contrib import admin

from .models import Cart, CartItem, Checkout, CheckoutItem


admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Checkout)
admin.site.register(CheckoutItem)
