from .models import UserProfile
from django.forms import ModelForm


class ProfileForm(ModelForm):
    """ 
    Provides required User data for User profile
    """

    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'saved_full_name': 'Full Name',
            'saved_email': 'Email Address',
            'saved_phone_number': 'Phone Number',
            'saved_address_line1': 'Address Line 1',
            'saved_address_line2': 'Address Line 2',
            'saved_region': 'Region or County',
            'saved_city': 'City or Town',
            'saved_postcode': 'Postal Code',
        }

        self.fields['saved_full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'saved_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'my-input'
            self.fields[field].label = False
