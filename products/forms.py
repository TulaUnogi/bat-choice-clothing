from django import forms
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = (
            'category', 'name', 'description',
            'condition', 'size', 'price',
            'primary_colour', 'secondary_colour',
            'image',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        display_names = [(c.display_name()) for c in categories]

        placeholders = {
            'category': 'Category',
            'name': 'Product Name',
            'description': 'Description',
            'condition': 'Condition of the product',
            'size': 'Size',
            'price': 'Price',
            'primary_colour': 'Primary Colour',
            'secondary_colour': 'Secondary Colour',
            'image': 'Product Image'
        }

        self.fields['category'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'category':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False