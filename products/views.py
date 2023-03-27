from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from . import models


class ProductContextMixin:

    """class get context for all categories to make it visible on each page"""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()
        return context


class StoreList(ProductContextMixin, ListView):

    """get only main photos, which is first of the product photo, to display it in the main store"""

    model = models.Products
    template_name = 'partials/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        return models.Products.objects.filter(productstock__is_active=True).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = models.Products.objects.all()
        context['main_product_image'] = [models.ProductImage.objects.filter(product=product).first() for product in products]
        print(context['main_product_image'])
        return context


class StoreProductDetail(ProductContextMixin, DetailView):

    """
    get first product photo, product stock and all photos of object which is displayed in  details, in method post
    validate product stock and if the user wants to buy more than in stock it will return message with error,
    setting session for cart
    """

    model = models.Products
    template_name = 'partials/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context['main_product_image'] = models.ProductImage.objects.filter(product=product).first()
        context['product_stock'] = models.ProductStock.objects.filter(product=product).all()
        context['images'] = models.ProductImage.objects.filter(product=product).all()
        return context

    def post(self, request, *args, **kwargs):
        product_slug = request.POST.get('product_slug')
        size = request.POST.get('size')
        quantity = int(request.POST.get('quantity', 1))
        product_stock = models.ProductStock.objects.get(product__slug=product_slug, size__name=size)
        price = float(product_stock.product.price)
        available_stock = product_stock.stock

        cart = request.session.get('cart', [])
        for cart_item in cart:
            if cart_item['product'] == product_slug and cart_item['size'] == size:
                current_quantity = cart_item['quantity']
                new_quantity = quantity + current_quantity
                if new_quantity > available_stock:
                    message = f"its only {available_stock} items available in stock"
                    messages.add_message(request, messages.ERROR, message)
                    return redirect('products:product-detail', slug=product_slug)
                else:
                    cart_item['quantity'] = new_quantity
                request.session['cart'] = cart
                return redirect(reverse_lazy('products:store'))
        if quantity > available_stock:
            message = f"Sorry, there are only {available_stock} items available in stock."
            messages.add_message(request, messages.ERROR, message)
            return redirect('products:product-detail', slug=product_slug)
        else:
            cart_item = {'product': product_slug, 'size': size, 'quantity': quantity, 'price': price}
            cart.append(cart_item)
            request.session['cart'] = cart
            return redirect(reverse_lazy('products:store'))


class StoreByCategory(ProductContextMixin, ListView):
    ''' search products by the category, get query set for category related to active products which are in it '''
    model = models.ProductStock
    template_name = 'partials/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = models.Category.objects.get(slug=self.kwargs['category_slug'])
        return models.Products.objects.filter(productstock__product__category=category,
                                              productstock__is_active=True).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = models.Products.objects.all()
        context['main_product_image'] = [models.ProductImage.objects.filter(product=product).first() for product in
                                         products]
        return context


