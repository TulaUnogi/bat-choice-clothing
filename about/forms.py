from django import forms
from .models import Review, RATING


class ReviewForm(forms.ModelForm):
    
    class Meta:
        model = Review
        fields = ('rating', 'order', 'order_review')

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['rating'].widget = forms.Select(choices=RATING)
        self.fields['order'] = forms.CharField(
            max_length=32, required=True, widget=forms.TextInput(attrs={
                'placeholder': 'Order Number *'}
            )
        )
        self.fields['order_review'].widget = forms.Textarea(
            attrs={'placeholder': 'Share your review here...'}
        )
