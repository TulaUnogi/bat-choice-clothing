from django.db import models


COLOURS = (
    ('BLACK', 'BLACK'),
    ('WHITE', 'WHITE'),
    ('YELLOW', 'YELLOW'),
    ('GREEN', 'GREEN'),
    ('RED', 'RED'),
    ('BLUE', 'BLUE'),
    ('PURPLE', 'PURPLE'),
    ('PINK', 'PINK'),
    ('ORANGE', 'ORANGE'),
    ('BROWN', 'BROWN'),
    ('GREY', 'GREY'),
    ('GOLD', 'GOLD'),
    ('COPPER', 'COPPER'),
    ('SILVER', 'SILVER'),
    ('MULTICOLOUR', 'MULTICOLOUR'),
)

CATEGORIES = (
    ('unknown category', 'unknown category'),
    ('tops', 'tops'),
    ('trousers', 'trousers'),
    ('skirts', 'skirts'),
    ('dresses', 'dresses'),
    ('footwear', 'footwear'),
    ('outerwear', 'outerwear'),
)


# Categories of Products
class Category(models.Model):
    name = models.CharField(max_length=100, choices=CATEGORIES, 
                            null=False, blank=False,
                            default='unknown category') 

    class Meta:
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return self.name

    def display_name(self):
        return f'--{self.name}--'


# Products
class Product(models.Model):
    category = models.ForeignKey('Category', null=False, blank=False, 
                                 default=1,
                                 on_delete=models.SET_DEFAULT)
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    condition = models.CharField(max_length=200, null=True, blank=True)
    size = models.CharField(max_length=20, null=True, blank=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    primary_colour = models.CharField(choices=COLOURS, default='BLACK', max_length=50)
    secondary_colour = models.CharField(choices=COLOURS, default='BLACK', max_length=50)
    image = models.ImageField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
