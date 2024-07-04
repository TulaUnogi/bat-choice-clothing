from django.contrib import admin
from checkout.models import OrderLineItem, Order, Discount


class OrderLineItemAdminInlines(admin.TabularInline):
    model = OrderLineItem
    readonly_fields = ('product_total',)


class OrderAdmin(admin.ModelAdmin):

    inlines = (OrderLineItemAdminInlines,)

    readonly_fields = ('order_number', 'order_date_time',
                       'order_total', 'shipping_cost',
                       'grand_total', 'discount_value')

    fields = ('order_number', 'user_profile','order_date_time',
              'order_total', 'shipping_cost',
              'grand_total','discount_value' , 'full_name', 'email', 
              'phone_number', 'address_line1',
              'address_line2', 'region', 'city', 
              'postcode', 'country', 'order_status',)
    
    list_display = ('order_number', 'order_date_time',
                    'order_total', 'shipping_cost',
                    'discount_value', 'grand_total',)

    ordering = ('-order_date_time',)

admin.site.register(Order, OrderAdmin)
admin.site.register(Discount)
