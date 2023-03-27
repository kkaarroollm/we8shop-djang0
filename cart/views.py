from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from cart.forms import ShippingAddressForm
from cart.models import Order, OrderItem, ShippingAddresses
from products import models
from products.models import ProductStock, ProductImage, Products


class CartView(View):

    ''' this Cart class displays products from the django session which were added in ProductDetailView,
        scanning the session it takes all information,
        search selected product and takes its name and image to display in cart:

        method get_context is a static method which retrieves data from django session

        '''

    @staticmethod
    def get_context(cart):
        items = []
        total = 0

        for cart_item in cart:
            product = ProductStock.objects.get(product__slug=cart_item['product'], size__name=cart_item['size'])
            product_img = ProductImage.objects.filter(product__slug=cart_item['product']).first()
            name = product.product.name
            size = cart_item['size']
            price = cart_item['price']
            quantity = cart_item['quantity']
            total += quantity * price

            item = {
                'name': name,
                'size': size,
                'quantity': quantity,
                'price': price,
                'image': product_img.image.url,
                'slug': product.product.slug
            }
            items.append(item)

        return {'items': items, 'total': total}

    '''i also update context with categories which are gonna display in CartView'''
    def get(self, request):
        cart = request.session.get('cart', [])
        context = self.get_context(cart)
        categories = models.Category.objects.all()
        context_items = {'categories': categories}
        context_items.update(context)
        print(context_items)
        return render(request, 'cart.html', context_items)

    '''while user  press the button  REMOVE in  cart, the product he wants to remove will decrease quantity by 1,  
    if the product reach quantity 0, the product will be deleted from car, which is item session'''

    def post(self, request):
        if 'remove' in request.POST:
            product_slug = request.POST.get('product')
            size_name = request.POST.get('size')

            cart = request.session.get('cart', [])

            for cart_item in cart:
                if cart_item['product'] == product_slug and cart_item['size'] == size_name:
                    cart_item['quantity'] -= 1
                    if cart_item['quantity'] == 0:
                        cart.remove(cart_item)
                    break

            request.session['cart'] = cart

        '''if the user press CHECKOUT button,  it validates if he's logged, if not it shows the ERROR,
         if he's logged, he's gonna be redirected to checkout view '''

        if 'checkout' in request.POST:
            cart = request.session.get('cart', [])
            context = self.get_context(cart)
            print(context)
            request.session['cart_context'] = context

            if not cart:
                message = "your cart is empty"
                messages.add_message(request, messages.ERROR, message)
                return redirect(reverse_lazy('cart:cart'))

            if request.user.is_authenticated:
                return redirect(reverse_lazy('cart:checkout'))
            else:
                message = "to go to checkout u gotta login"
                messages.add_message(request, messages.ERROR, message)
                return redirect(reverse_lazy('cart:cart'))
        return redirect('cart:cart')


class CheckoutView(LoginRequiredMixin, View):
    '''in method get, the user is prompted to fill the form of shipping,
    also there is context passed from session 'cart_context', i updated it by categories as well to display them also in checkout view.

     in the method post, when user fills the form properly and press PLACE ORDER button,
      he will be redirected to the homepage. the method will the information from the ShippingAddressForm
       and save it to the db. Each item he order it will save to OrderItem  table,
       and the data of the whole order with calculating total price in table Order.
       After that the session 'cart' gonna be deleted'''
    def get(self, request):
        form = ShippingAddressForm()
        categories = models.Category.objects.all()
        cart_context = request.session.get('cart_context')
        context = {'form': form,  'categories': categories}
        if cart_context:
            context.update(cart_context)

        return render(request, 'checkout.html', context)

    def post(self, request):
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            cart = request.session.get('cart', [])
            total = sum(item['quantity'] * item['price'] for item in cart)
            order = Order(
                customer=request.user,
                total_price=total
            )
            order.save()

            shipping_address = ShippingAddresses(
                customer=request.user,
                order=order,
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                state=form.cleaned_data['state'],
                zipcode=form.cleaned_data['zipcode']
            )
            shipping_address.save()

            for cart_item in cart:
                product = Products.objects.get(slug=cart_item['product'])
                product_size = ProductStock.objects.get(product=product, size__name=cart_item['size']).size
                order_item = OrderItem(
                    order=order,
                    product=product,
                    size=product_size,
                    quantity=cart_item['quantity'],
                    price=cart_item['price']
                )
                order_item.save()

            del request.session['cart']
            return redirect('home:homepage')





