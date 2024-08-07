from django.db import models
from django.db.models import Sum
from django.conf import settings
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

from products.models import Product
from userprofile.models import UserProfile

from decimal import Decimal
from django_countries.fields import CountryField
import uuid


ORDER_STATUS = (
    ("Awaiting Fulfillment", "Awaiting Fulfillment"),
    ("Awaiting Shipment", "Awaiting Shipment"),
    ("Order Shipped", "Order Shipped"),
    ("Order Completed", "Order Completed"),
    ("Cancelled", "Cancelled"),
    ("Refunded", "Refunded"),
    ("Partially Refunded", "Partially Refunded"),
    ("Disputed", "Disputed"),
)


class Discount(models.Model):
    """Stores active discount codes and their values"""

    discount_code = models.CharField(max_length=30, null=True, blank=True,
        	                         unique=True)
    percent = models.PositiveIntegerField(null=False, default=0,
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.percent}% off with code: {self.discount_code}'


class Order(models.Model):
    """
    Stores all customer order data and calculates order total
    """
    
    order_date_time = models.DateTimeField(auto_now_add=True)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders')
    full_name = models.CharField(max_length=100, null=False, blank=False, default="")
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(
        max_length=17, blank=True, null=True, validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$', 
            message="Phone number must be entered in the format: '+123456789'.\
                     Up to 15 digits allowed.",
            code="invalid")])
    address_line1 = models.CharField(max_length=200, null=False, blank=False, 
                                     default="")
    address_line2 = models.CharField(max_length=200, null=False, blank=False, 
                                     default="")
    region = models.CharField(max_length=85, null=False, blank=False)
    city = models.CharField(max_length=85, null=False, blank=False)
    postcode = models.CharField(
        max_length=30, null=True, blank=True, validators=[RegexValidator(
            regex=r'^[\d\-a-zA-Z]+$',
            message="Only letters, numbers and hyphens allowed.",
            code="invalid")])
    country = CountryField(blank_label="Country *", null=False, blank=False)
    order_number = models.CharField(max_length=32, null=False, unique=True,
                                    db_index=True, editable=False)
    order_status = models.CharField(choices=ORDER_STATUS, max_length=40, null=False,
                                    blank=False, default="Awaiting Fulfillment")
    order_subtotal = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, default=0)
    discount = models.ForeignKey(Discount, null=True, blank=True,
                                    on_delete=models.CASCADE,
                                    related_name="discount") # one code per order
    discount_value = models.DecimalField(max_digits=6, decimal_places=2,
                                      null=False, default=0)
    order_total = models.DecimalField(max_digits=6, decimal_places=2,
                                      null=False, default=0)
    shipping_cost = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    grand_total = models.DecimalField(max_digits=6, decimal_places=2,
                                      null=False, default=0)

    def update_order_subtotal(self):

        """
        Calculate order subtotal 
        (from Code Institute Boutique Ado walktrough)
        """
        self.order_subtotal = self.lineitems.aggregate(Sum("product_total"))[
            "product_total__sum"
        ] or 0
        self.save()
        return self.order_subtotal

    def update_discounted_total(self):
        # Calculate discount value
        if self.discount:
            self.discount_value = self.order_subtotal * Decimal(self.discount.percent / 100)
        else:
            self.discount_value = 0
        # Calculate total
        self.order_total = self.order_subtotal - self.discount_value
        self.save()
        return self.order_total

    def update_shipping_cost(self):
        # Calculate shipping costs
        if self.order_subtotal < settings.FREE_SHIPPING_TRESHOLD:
            if self.order_subtotal >= settings.MINIMUM_SHIPPING_COST:
                self.shipping_cost = (self.order_subtotal 
                                    * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE
                                                / 100))
            if self.shipping_cost < settings.MINIMUM_SHIPPING_COST:
                self.shipping_cost = settings.MINIMUM_SHIPPING_COST
        else:
            self.shipping_cost = 0
        self.save()
        return self.shipping_cost

    def update_grand_total(self):
        # Calculate grand total
        self.grand_total = self.order_total + self.shipping_cost
        self.save()
        return self.grand_total

    def _create_order_number(self):
        """Use UUID to create a unique order number"""

        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the default save to set the order 
        number if it wasn't there yet.
        From Boutique Ado walktrough.
        """

        if not self.order_number:
            self.order_number = self._create_order_number()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    """
    Stores ordered product data
    """
    order = models.ForeignKey(Order, null=False, blank=False, 
                              on_delete=models.CASCADE, related_name="lineitems")
    product = models.ForeignKey(Product, null=False, blank=False,
                                on_delete=models.CASCADE)
    product_total = models.DecimalField(max_digits=6, decimal_places=2,
                                        null=False, default=0)
    product_quantity = models.IntegerField(default=1, null=False) #single items only

    def save(self, *args, **kwargs):
        """
        Override default save function to set the product_total.
        """
        self.product_total = self.product.price * self.product_quantity
        super().save(*args, **kwargs)
