from django.contrib import admin

from cart.models import ShippingAddresses, Order, OrderItem


class OrderItemInline(admin.TabularInline):
    fields = ('product', 'size', 'quantity')
    model = OrderItem
    extra = 1


class ShippingAddressesInline(admin.TabularInline):
    model = ShippingAddresses
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'status', 'created_at', 'updated_at', 'total_price')
    inlines = [OrderItemInline, ShippingAddressesInline]


@admin.register(ShippingAddresses)
class ShippingAddressesAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'order', 'address', 'city', 'state', 'zipcode')

