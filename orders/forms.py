"""Forms for the orders app."""
from django import forms

from .models import Order, MenuItem, MenuCategory


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


class MenuItemForm(forms.ModelForm):
    """Form for adding/editing menu items."""

    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'image', 'is_available', 'is_featured', 'tag']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'e.g., Chicken Burger'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Describe the dish...',
                'rows': 3
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
            'image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500',
                'accept': 'image/*'
            }),
            'tag': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500'
            }),
        }
