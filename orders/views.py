from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.views.generic import ListView, TemplateView

from .cart import Cart
from .models import MenuCategory, MenuItem


class HomeView(TemplateView):
    """Landing page where customers will browse a preview of the menu."""

    template_name = 'orders/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = MenuCategory.objects.all()
        items = MenuItem.objects.filter(is_available=True)[:6]

        context["categories"] = categories
        context["menu_items"] = items
        context["selected_category"] = None
        context["selected_tag"] = None
        return context


class MenuListView(ListView):
    """Full menu page with filters by category/tag."""

    model = MenuItem
    context_object_name = 'menu_items'

    def get_template_names(self):
        """Use dashboard layout if user is logged in."""
        if self.request.user.is_authenticated:
            return ['orders/menu_list_dashboard.html']
        return ['orders/menu_list.html']

    def get_queryset(self):
        qs = MenuItem.objects.filter(is_available=True)
        self.selected_category = self.request.GET.get("category") or ""
        self.selected_tag = self.request.GET.get("tag") or ""

        if self.selected_category:
            qs = qs.filter(category__slug=self.selected_category)
        if self.selected_tag in {choice[0] for choice in MenuItem.Tags.choices}:
            qs = qs.filter(tag=self.selected_tag)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = MenuCategory.objects.all()
        context["selected_category"] = self.selected_category
        context["selected_tag"] = self.selected_tag
        return context



# Cart Views
@require_POST
def add_to_cart(request, menu_item_id):
    """Add a menu item to the cart."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to add items to cart.')
        return redirect('login')
    
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.add(menu_item=menu_item, quantity=quantity)
    messages.success(request, f'{menu_item.name} added to cart!')
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'message': f'{menu_item.name} added to cart!'
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'orders:home'))


@login_required
def view_cart(request):
    """Display the shopping cart."""
    cart = Cart(request)
    template = 'orders/cart_dashboard.html' if request.user.is_authenticated else 'orders/cart.html'
    return render(request, template, {'cart': cart})


@require_POST
def update_cart(request, menu_item_id):
    """Update the quantity of a menu item in the cart."""
    cart = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    
    cart.update_quantity(menu_item_id, quantity)
    messages.success(request, 'Cart updated!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })
    
    return redirect('orders:cart')


@require_POST
def remove_from_cart(request, menu_item_id):
    """Remove a menu item from the cart."""
    cart = Cart(request)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    
    cart.remove(menu_item)
    messages.success(request, f'{menu_item.name} removed from cart!')
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_total': str(cart.get_total_price())
        })
    
    return redirect('orders:cart')


def clear_cart(request):
    """Clear all items from the cart."""
    cart = Cart(request)
    cart.clear()
    messages.success(request, 'Cart cleared!')
    return redirect('orders:cart')



# Checkout Views
def checkout(request):
    """Checkout page for placing orders."""
    if not request.user.is_authenticated:
        messages.warning(request, 'Please login to checkout.')
        return redirect('login')
    
    cart = Cart(request)
    
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty!')
        return redirect('orders:cart')
    
    if request.method == 'POST':
        from .forms import CheckoutForm
        from .models import Order, OrderItem
        
        form = CheckoutForm(request.POST)
        
        if form.is_valid():
            # Create order
            order = form.save(commit=False)
            order.user = request.user
            order.delivery_location = request.user.workplace
            order.phone = request.user.phone
            order.total_amount = cart.get_total_price()
            order.save()
            
            # Create order items
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    menu_item=item['menu_item'],
                    quantity=item['quantity'],
                    price=item['price']
                )
            
            # Clear cart
            cart.clear()
            
            messages.success(request, 'Your order has been placed successfully!')
            return redirect('orders:order_success', order_id=order.id)
    else:
        from .forms import CheckoutForm
        form = CheckoutForm()
    
    return render(request, 'orders/checkout.html', {
        'form': form,
        'cart': cart
    })


def order_success(request, order_id):
    """Order confirmation page."""
    from .models import Order
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})


# Dashboard Views
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count

@login_required
def dashboard(request):
    """Customer dashboard home."""
    from .models import Order
    
    # Get user statistics
    orders = Order.objects.filter(user=request.user)
    total_orders = orders.count()
    pending_orders = orders.filter(status__in=['pending', 'confirmed', 'preparing']).count()
    total_spent = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Get recent orders
    recent_orders = orders.order_by('-created_at')[:5]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'orders/dashboard.html', context)


@login_required
def order_history(request):
    """Customer order history."""
    from .models import Order
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def profile(request):
    """Customer profile page."""
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.phone = request.POST.get('phone', '')
        user.workplace = request.POST.get('workplace', '')
        user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('orders:profile')
    
    return render(request, 'orders/profile.html')
