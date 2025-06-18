from django.urls import path

from .views import add_to_cart, remove_from_cart, cart_view, checkout_view


urlpatterns = [
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart'),
    path('checkout/', checkout_view, name='checkout'),
]
