from django.contrib import admin
from checkout.models import OrderLineItem, Order


class OrderLineItemAdminInlines(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('product_total',)


class OrderAdmin(admin.ModelAdmin):

    inlines = (OrderLineItemAdminInlines,)

    readonly_fields = ('order_number', 'order_date_time',
                       'order_total', 'shipping_cost',
                       'grand_total',)

    fields = ('order_number','order_date_time',
              'order_total', 'shipping_cost',
              'grand_total', 'first_name', 'last_name',
              'email', 'phone_number', 'address_line1',
              'address_line2', 'address_line3',
              'region', 'city', 'postcode', 'country',
              'order_status',)
    
    list_display = ('order_number', 'order_date_time',
                    'order_total', 'shipping_cost',
                       'grand_total',)

    ordering = ('-order_date_time',)

admin.site.register(Order, OrderAdmin)
