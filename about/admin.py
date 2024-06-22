from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = [
        'customer', 'order', 'rating', 'review_date', 'order_review',
    ]

    fields = [
        'customer', 'order', 'rating', 'review_date', 'order_review',
    ]

    list_display = [
        'customer', 'order', 'rating', 'review_date', 'order_review',
    ]

    ordering = ('-review_date',)

admin.site.register(Review, ReviewAdmin)
