from django import forms
from .models import ShippingAddresses


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddresses
        fields = ['address', 'city', 'state', 'zipcode']
        labels = {
            'address': 'Address',
            'city': 'City',
            'state': 'State',
            'zipcode': 'Zip Code',
        }
