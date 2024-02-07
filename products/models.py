from django.db import models


# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=100)
    friendly_name = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def return_friendly(self):
        return self.friendly_name


# Products
class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    condition = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
