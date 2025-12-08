"""Forms for the orders app."""
from django import forms

from .models import Order, MenuItem, MenuCategory, ContactInquiry


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



class ContactForm(forms.ModelForm):
    """Form for submitting contact inquiries."""
    
    class Meta:
        model = ContactInquiry
        fields = ['name', 'email', 'phone', 'subject_type', 'order_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Your full name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'your.email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': '+254 700 000 000'
            }),
            'subject_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'id': 'id_subject_type'
            }),
            'order_number': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'ORD-20240101-0001',
                'id': 'id_order_number'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary focus:border-primary',
                'placeholder': 'Tell us more about your inquiry...',
                'rows': 5
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'subject_type': 'Subject',
            'order_number': 'Order Number (Optional)',
            'message': 'Message',
        }
    
    def clean_order_number(self):
        """Validate order number if provided."""
        order_number = self.cleaned_data.get('order_number')
        subject_type = self.cleaned_data.get('subject_type')
        
        if order_number and subject_type == 'order_inquiry':
            # Optionally validate that order exists
            if not Order.objects.filter(order_number=order_number).exists():
                raise forms.ValidationError("Order number not found in our system.")
        
        return order_number
