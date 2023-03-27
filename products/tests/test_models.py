import pytest
from products.models import Products, ProductStock, SizeOption


@pytest.mark.django_db
def test_create_products_model():
    product = Products.objects.create(name='test', description='test', price=23.23)
    assert product.slug == 'test'


@pytest.mark.django_db
def test_create_productstock_model():
    product = Products.objects.create(name='test', description='test', price=23.23)
    size = SizeOption.objects.create(name='small')
    product_stock = ProductStock.objects.create(product=product, size=size, stock=10)
    assert product_stock.is_active is True


@pytest.mark.django_db
def test_productstock_model_set_active_status():
    product = Products.objects.create(name='test', description='test', price=23.23)
    size = SizeOption.objects.create(name='small')
    product_stock = ProductStock.objects.create(product=product, size=size, stock=0)
    product_stock.set_active_status()
    assert product_stock.is_active is False


@pytest.mark.django_db
def test_productstock_model_save():
    product = Products.objects.create(name='test', description='test', price=23.23)
    size = SizeOption.objects.create(name='small')
    product_stock = ProductStock.objects.create(product=product, size=size, stock=0)
    assert product_stock.is_active is False
    product_stock.stock = 10
    product_stock.save()
    assert product_stock.is_active is True


