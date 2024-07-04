from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Cart, Order, OrderItem
from products.models import Product
from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from django.views import View
from .forms import OrderForm
from user.models import CustomUserProfile

def add_to_cart(request, id):
    if request.user.is_authenticated:
        user = request.user
        product = Product.objects.get(id=id)

        existing_item = Cart.objects.filter(user=user, product=product).first()
        if existing_item:
            existing_item.quantity += 1
            existing_item.save()
        else:
            Cart.objects.create(user=user, product=product)
        return redirect('/cart')
    else:
        session_id = request.session.get('session_id')
        product = Product.objects.get(id=id)

        existing_item = Cart.objects.filter(guest_session_id=session_id, product=product).first()
        if existing_item:
            existing_item.quantity += 1
            existing_item.save()
        else:
            Cart.objects.create(guest_session_id=session_id, product=product)

        messages.debug(request, "Item added to cart")
        return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
    else:
        session_id = request.session.get('session_id')
        cart = Cart.objects.filter(guest_session_id=session_id)

    amount = Decimal(0.0)
    shipping_amount = Decimal(500.0)
    total_amount = 0.0

    cart_product = [p for p in cart]
    if cart_product:
        for p in cart_product:
            tempamount = Decimal(p.quantity * p.product.discounted_price)
            amount += tempamount  
            subtotal = tempamount
        total_amount = amount + shipping_amount
        return render(request, 'order/cart.html', {'cart': cart, 'totalamount': total_amount, 'amount': amount, 'shippingamount': shipping_amount, 'subtotal': subtotal})
    else:
        return render(request, 'order/empty_cart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        if request.user.is_authenticated:
            cart_obj = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        else:
            session_id = request.session.get('session_id')
            cart_obj = Cart.objects.filter(guest_session_id=session_id, product=prod_id).first()
        
        if cart_obj:
            cart_obj.quantity += 1
            cart_obj.save()
        else:
            if request.user.is_authenticated:
                Cart.objects.create(user=request.user, product=Product.objects.get(id=prod_id))
            else:
                session_id = request.session.get('session_id')
                Cart.objects.create(guest_session_id=session_id, product=Product.objects.get(id=prod_id))
          
        amount = Decimal(0.0)
        shipping_amount = Decimal(500.0)
        total_amount = 0.0

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
        else:
            guest_cart = request.session.get('session_id')
            cart = Cart.objects.filter(guest_session_id=guest_cart)

        cart_product = [p for p in cart]
        if cart_product:
            for p in cart_product:
                tempamount = Decimal(p.quantity * p.product.discounted_price)
                amount += tempamount
                subtotal = tempamount
            total_amount = amount + shipping_amount
        
        data = {
            'quantity': cart_obj.quantity,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        if request.user.is_authenticated:
            cart_obj = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        else:
            guest_cart = request.session.get('session_id')
            cart_obj = Cart.objects.filter(guest_session_id=guest_cart, product=prod_id).first()
        
        if cart_obj and cart_obj.quantity >= 2:
            cart_obj.quantity -= 1
            cart_obj.save()
        
        amount = Decimal(0.0)
        shipping_amount = Decimal(500.0)
        total_amount = 0.0

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
        else:
            guest_cart = request.session.get('session_id')
            cart = Cart.objects.filter(guest_session_id=guest_cart)

        cart_product = [p for p in cart]
        if cart_product:
            for p in cart_product:
                tempamount = Decimal(p.quantity * p.product.discounted_price)
                amount += tempamount
                subtotal = tempamount
            total_amount = amount + shipping_amount
        
        data = {
            'quantity': cart_obj.quantity if cart_obj else 0,
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        
        if request.user.is_authenticated:
            cart_obj = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user)).first()
        else:
            guest_cart = request.session.get('session_id')
            cart_obj = Cart.objects.filter(guest_session_id=guest_cart, product=prod_id).first()
        
        if cart_obj:
            cart_obj.delete()
        
        amount = Decimal(0.0)
        shipping_amount = Decimal(500.0)
        total_amount = 0.0

        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=request.user)
        else:
            guest_cart = request.session.get('session_id')
            cart = Cart.objects.filter(guest_session_id=guest_cart)

        cart_product = [p for p in cart]
        if cart_product:
            for p in cart_product:
                tempamount = Decimal(p.quantity * p.product.discounted_price)
                amount += tempamount
                subtotal = tempamount
            total_amount = amount + shipping_amount
        
        data = {
            'amount': amount,
            'totalamount': total_amount
        }
        return JsonResponse(data)

class Checkout(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)
            profile = CustomUserProfile.objects.filter(user=user).first()
        else:
            guest_cart = request.session.get('session_id')
            cart = Cart.objects.filter(guest_session_id=guest_cart)
            profile = None  # Set profile to None if user is not authenticated

        amount = Decimal(0.0)
        shipping_amount = Decimal(500.0)
        total_amount = 0.0
        subtotal = 0

        cart_product = [p for p in cart]
        if cart_product:
            for p in cart_product:
                tempamount = Decimal(p.quantity * p.product.discounted_price)
                amount += tempamount
                subtotal += tempamount  # Calculate subtotal
            total_amount = amount + shipping_amount
            return render(request, 'order/checkout.html', {'totalamount': total_amount, 'amount': amount, 'shippingamount': shipping_amount, 'subtotal': subtotal, 'profile': profile})
        else:
            return redirect('/cart')
    

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_note = request.POST.get('order_note')

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address=address,
                country=country,
                company=company,
                city=city,
                order_note=order_note
            )
        else:
            order = Order.objects.create(
                guest_session_id=request.session.get('session_id'),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address=address,
                country=country,
                company=company,
                city=city,
                order_note=order_note
            )

        cart_products = Cart.objects.filter(user=request.user) if request.user.is_authenticated else Cart.objects.filter(guest_session_id=request.session.get('session_id'))

        for product in cart_products:
            order_item = OrderItem.objects.create(
                order=order,
                product=product.product,
                quantity=product.quantity,
                product_price=product.product.discounted_price
            )

        if request.user.is_authenticated:
            Cart.objects.filter(user=request.user).delete()
        else:
            Cart.objects.filter(guest_session_id=request.session.get('session_id')).delete()

        return render(request, "order/confirmation.html")

class DirectCheckout(View):
    def get(self, request, id):
        product = Product.objects.get(id=id)
        amount = product.discounted_price
        shipping_amount = Decimal(500)
        total_amount = amount + shipping_amount

        if request.user.is_authenticated:
            profile = CustomUserProfile.objects.filter(user=request.user).first()
        else:
            profile = None  

        return render(request, 'order/checkout.html', {'totalamount': total_amount, 'amount': amount, 'shippingamount': shipping_amount, 'product': product, 'profile': profile})

    def post(self, request, id):
        product = Product.objects.get(id=id)
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        company = request.POST.get('company')
        country = request.POST.get('country')
        address = request.POST.get('address')
        city = request.POST.get('city')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        order_note = request.POST.get('order_note')

        if request.user.is_authenticated:
            order = Order.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address=address,
                country=country,
                company=company,
                city=city,
                order_note=order_note
            )
        else:
            order = Order.objects.create(
                guest_session_id=request.session.get('session_id'),
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                address=address,
                country=country,
                company=company,
                city=city,
                order_note=order_note
            )

        order_item = OrderItem.objects.create(
            order=order,
            product=product,
            quantity=product.quantity,
            product_price=product.discounted_price
        )
        
        return render(request, "order/confirmation.html")

def order_history(request):
    if request.user.is_authenticated:
        order_objects = Order.objects.filter(user=request.user)
    else:
        order_objects = Order.objects.filter(guest_session_id=request.session.get('session_id'))
    orders = []
    for order_object in order_objects:
        products = OrderItem.objects.filter(order=order_object)
        subtotal = Decimal(0.0)

        for product in products:
            subtotal += product.quantity * product.product_price

        orders.append({"order": order_object, "products": products, "subtotal": subtotal})

    return render(request, "order/order_history.html", {"orders": orders})
