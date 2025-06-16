from django.db import models

from django.contrib.auth.models import User
from apps.shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart_user')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def cart_sub_total_price(self):
        return int(sum(item.product.price * item.quantity for item in self.cartitem_cart.all()))

    @property
    def cart_total_price(self):
        return int(sum(item.product.discount * item.quantity for item in self.cartitem_cart.all()))
    
    class Meta:
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'

    def __str__(self):
        return f"ID: {self.pk} - Cart - User: {self.user.username} - Sub Total: {self.cart_sub_total_price} - Total: {self.cart_total_price}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem_cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitem_product')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    @property
    def total_price(self):
        return int(self.product.discount * self.quantity)

    def __str__(self):
        return f'ID: {self.pk} - Cart: {self.cart} - Product: {self.product.name} - Quantity: {self.quantity} - Total Price: {self.total_price}'


class Checkout(models.Model):
    STATUS = (
        ('new', 'New'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkout_user')
    status = models.CharField(max_length=100, choices=STATUS, default='new')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'

    def __str__(self):
        return f"ID: {self.pk} - User: {self.user.username} - Status: {self.status}"


class CheckoutItem(models.Model):
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE, related_name='checkoutitem_checkout')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='checkoutitem_product')
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Checkout Item'
        verbose_name_plural = 'Checkout Items'
        unique_together = ('checkout', 'product')

    def __str__(self):
        return f"ID: {self.pk} - Checkout: {self.checkout.pk} - Product: {self.product.name} - Quantity: {self.quantity} - Price: {self.price}"
