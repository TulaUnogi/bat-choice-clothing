from django.db import models
from userprofile.models import UserProfile

RATING = (
    (1, 'Excellent',),
    (2, 'Good',),
    (3, 'Average',),
    (4, 'Bad',),  
    (5, 'Terrible',),
)

class Review(models.Model):
    customer = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    order = models.CharField(max_length=32, null=False, blank=False)
    rating = models.PositiveIntegerField(choices=RATING)
    review_date = models.DateTimeField(auto_now_add=True)
    order_review = models.TextField(max_length=1000)

    class Meta:
        unique_together = ('customer', 'order')

    def __str__(self):
        return f"{self.customer}'s review for order {self.order}"