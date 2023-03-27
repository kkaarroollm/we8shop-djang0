import pytest
from django.core.exceptions import ValidationError
from cart.models import Order, OrderItem, ShippingAddresses
from products.models import ProductStock, SizeOption, Products


@pytest.fixture
def order():
    return Order.objects.create()


@pytest.fixture
def product():
    return Products.objects.create(name='test', price=10.00)


@pytest.fixture
def size_option():
    return SizeOption.objects.create(name='small')


@pytest.mark.django_db
def test_order_item_clean_with_stock_over_stock(order, product, size_option):
    ProductStock.objects.create(product=product, size=size_option, stock=0)
    item = OrderItem(order=order, product=product, size=size_option, quantity=2)
    with pytest.raises(ValidationError) as err:
        item.clean()
    assert f'{product.name} is not available in size {size_option}' in str(err.value)


@pytest.mark.django_db
def test_order_item_clean_with_excessive_quantity(order, product, size_option):
    ProductStock.objects.create(product=product, size=size_option, stock=5)
    item = OrderItem(order=order, product=product, size=size_option, quantity=10)
    with pytest.raises(ValidationError) as err:
        item.clean()
    assert f'stock of {product.name} ({size_option}) has only 5 available' in str(err.value)


@pytest.mark.django_db
def test_order_item_clean_with_sufficient_stock(order, product, size_option):
    ProductStock.objects.create(product=product, size=size_option, stock=5)
    item = OrderItem(order=order, product=product, size=size_option, quantity=3)
    item.clean()
    assert item.price == product.price


@pytest.mark.django_db
def test_update_product_stock_signal_with_new_order_item(order, product, size_option):
    ProductStock.objects.create(product=product, size=size_option, stock=5)
    OrderItem.objects.create(order=order, product=product, size=size_option, quantity=2, price=product.price)
    stock = ProductStock.objects.get(product=product, size=size_option)
    assert stock.stock == 3


def test_shipping_address_str():
    address = ShippingAddresses(address='test', city='test', state='NJ', zipcode='00000')
    assert str(address) == 'test'

