from django.db import models
from userprofile.models import UserProfile
from checkout.models import Order

RATING = (
    (1, '1 star',),
    (2, '2 stars',),
    (3, '3 stars',),
    (4, '4 stars',),
    (5, '5 stars',),
)

class Review(models.Model):
    customer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL,
                                      null=True, blank=True)
    rating = models.PositiveIntegerField(choices=RATING)
    review_date = models.DateTimeField(auto_now_add=True)
    order_review = models.TextField(max_length=1000)

    class Meta:
        unique_together = ('customer', 'order')

    def __str__(self):
        return f"{self.customer}'s {self.rating}- star rating for order {self.order.order_number}"