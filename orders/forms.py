"""Forms for the orders app."""
from django import forms

from .models import Order


class CheckoutForm(forms.ModelForm):
    """Form for checkout process."""

    class Meta:
        model = Order
        fields = ['payment_method', 'notes']
        widgets = {
            'payment_method': forms.RadioSelect(attrs={
                'class': 'space-y-2'
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full rounded-lg border border-gray-300 px-4 py-2 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary',
                'placeholder': 'Any special instructions? (Optional)',
                'rows': 3
            }),
        }
