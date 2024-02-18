from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models import Sum
import uuid


class Order(models.Model):
    """ Stores all customer order data """
    
    order_date_time = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(max_length=19, null=False, blank=False)
    address_line1 = models.CharField(max_length=70, null=False, blank=False)
    address_line2 = models.CharField(max_length=70, null=False, blank=False)
    address_line3 = models.CharField(max_length=70, null=True, blank=True)
    region = models.CharField(max_length=85, null=False, blank=False)
    city = models.CharField(max_length=85, null=False, blank=False)
    postcode = models.CharField(max_length=30, null=True, blank=True)
    country = models.CharField(max_length=56, null=False, blank=False)
    order_number = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True, editable=False)
    order_status = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.order_number


class OrderLine(models.Model):    
    """ Stores data related to calculated order totals """

    order = models.ForeignKey(Order, null=False, blank=False, on_delete=models.CASCADE)
    order_line_items = models.ForeignKey(Product, null=False, blank=False, 
                                         on_delete=models.CASCADE, 
                                         related_name='lineitems')
    order_subtotal = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    order_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    discount = models.OneToOneField(Discount, on_delete=models.CASCADE, 
                                           related_name='discount') # one code per order
    grand_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, default=0)

    def update_order_totals(self):

        # Calculate order subtotal (from Code Institute Boutique Ado walktrough)
        self.order_subtotal = self.lineitems.aggregate(Sum('product_total'))['product_total__sum']
        
        # Calculate discount value
        if self.discount.code:
            discount_value = (self.subtotal * self.discount.percent) / 100
        else:
            discount_value = 0

        # Calculate shipping costs
        if self.order_subtotal < settings.FREE_SHIPPING_THRESHOLD:
            self.shipping_cost = self.order_subtotal * settings.STANDARD_DELIVERY_PERCENTAGE / 100
            if self.shipping_cost < settings.MINIMUM_SHIPPING_COST:
                self.shipping_cost = settings.MINIMUM_SHIPPING_COST
        else:
            self.shipping_cost = 0

        # Calculate total
        self.order_total = self.order_subtotal - discount_value

        # Calculate grand total
        self.grand_total = self.order_total + self.delivery_cost

    def create_order_number(self):
        """ Use UUID to create a unique order number"""

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """ 
        Override the default save to set the order number if it wasn't there yet.
        From Boutique Ado walktrough.
        """

        if not self.order_number:
            self.order_number = self._create_order_number()
            super().save(*args, **kwargs)

    def __str__(self):
        return f'Order grand total: {self.grand_total}€'


class Discount(models.Model):
    """ Stores active discount codes and their values """

    code = models.CharField(max_length=30, null=True, blank=True)
    percent = models.PositiveIntegerField(max_digits=2, null=True, default=0)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.discount_percent}% off with code: {self.discount_code}'


class OrderLineItem(models.Model):
    """ Stores ordered product data """
    product = ForeignKey(Product, null=False, blank=False, on_delete=models.CASCADE)
    product_total = DecimalField(max_digits=6, decimal_places=2, null=False, default=0)
    product_quantity = IntegerField(default=1, max=1, min=1, null=False) #single items only

    def save(self, *args, **kwargs):
        """ Overrides the default save to set total """
        self.product_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_total
