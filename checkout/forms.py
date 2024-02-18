from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'email',
            'phone_number', 'address_line1',
            'address_line2', 'address_line3',
            'region', 'city', 'postcode', 'country',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'address_line3': 'Address Line 3',
            'region': 'Region or County',
            'city': 'City or Town',
            'postcode': 'Postal Code',
            'country': 'Country',            
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
