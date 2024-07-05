from django.contrib import admin
from .models import Category, Product



class ProductAdmin(admin.ModelAdmin):

    readonly_fields= (
        'name', 'category', 'price', 'availability'
    )

    list_filter = ('availability','size', 'category')

    ordering = ('-added_on',)

admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
