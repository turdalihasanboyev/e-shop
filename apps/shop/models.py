from django.db import models

import uuid

from django.contrib.auth.models import User

from django.db.models import Avg

from django.core.validators import MinValueValidator, MaxValueValidator

from django.urls import reverse

from datetime import datetime

from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) # base slug
            # uuid_slug = uuid.uuid4().hex[:8] # kalta variant 8talik
            uuid_slug = uuid.uuid4() # uzun variant tolliq
            # date_slug = datetime.now().strftime("%d-%m-%Y") # Natija: kun-oy-yil (kalta)
            date_slug = datetime.today().strftime("%d-%m-%Y-%H-%M-%S") # kun-oy-yil-soat-minut-sekund # uzun tolliq variant
            self.slug = f"{base_slug}-{uuid_slug}-{date_slug}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"ID: {self.pk} - Name: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=500, unique=True, null=True, blank=True)
    image = models.ImageField(upload_to='product_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product_category')
    price = models.PositiveIntegerField(default=0)
    percentage = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discount(self):
        if self.percentage:
            discount_amount = int((self.price * self.percentage) / 100)
            return int(self.price - discount_amount)
        return int(self.price)

    @property
    def average_rating(self):
        average = self.review_product.aggregate(avg_rate=Avg('rate'))['avg_rate']
        return round(average, 2) if average else 0

    def save(self, *args, **kwargs):
        if not self.slug:
            uuid_slug = uuid.uuid4()
            self.slug = f"{uuid_slug}"
        super().save(*args, **kwargs)

    def get_absolute_url(self, *args, **kwargs):
        return reverse('product_detail', kwargs={'product_slug': self.slug})

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return f"ID: {self.pk} - Name: {self.name} - Image: {self.image} - Category: {self.category.name} - Price: {self.price} - Percentage: {self.percentage} - Views: {self.views} - Discount: {self.discount} - Rating: {self.average_rating}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review_product')
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True, max_length=100)
    review = models.TextField(null=True, blank=True)
    rate = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"ID: {self.pk} - User: {self.user.username} - Product: {self.product.name} - Rate: {self.rate}"
