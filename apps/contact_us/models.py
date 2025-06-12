from django.db import models


class ContactUS(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Contact Us'
        verbose_name_plural = 'Contact Us'

    def __str__(self):
        return f"ID: {self.pk} - Name: {self.name} - Email: {self.email}"
