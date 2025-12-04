from django.contrib import admin

from .models import MenuCategory, MenuItem, Order, OrderItem


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
  list_display = ("name", "is_featured")
  list_filter = ("is_featured",)
  prepopulated_fields = {"slug": ("name",)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
  list_display = ("name", "category", "price", "is_available", "tag")
  list_filter = ("category", "is_available", "tag")
  search_fields = ("name", "description")
  list_editable = ("price", "is_available", "tag")



class OrderItemInline(admin.TabularInline):
  """Inline admin for order items."""

  model = OrderItem
  extra = 0
  readonly_fields = ("menu_item", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
  """Admin for orders."""

  list_display = ("order_number", "user", "status", "payment_method", "total_amount", "created_at")
  list_filter = ("status", "payment_method", "created_at")
  search_fields = ("order_number", "user__username", "user__email", "delivery_location")
  list_editable = ("status",)
  readonly_fields = ("order_number", "created_at", "updated_at")
  inlines = [OrderItemInline]

  fieldsets = (
    ("Order Info", {"fields": ("order_number", "user", "status", "total_amount")}),
    ("Delivery Details", {"fields": ("delivery_location", "phone", "notes")}),
    ("Payment", {"fields": ("payment_method",)}),
    ("Timestamps", {"fields": ("created_at", "updated_at")}),
  )
