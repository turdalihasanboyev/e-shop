from django.db import models

import uuid

from datetime import datetime

from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=250, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
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
