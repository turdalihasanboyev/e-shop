from django.urls import path

from .views import shop_view, product_detail_view


urlpatterns = [
    path('shop/', shop_view, name='shop'),
    path('product/<slug:product_slug>/detail/', product_detail_view, name='product_detail'),
]
