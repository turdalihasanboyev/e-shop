from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse

from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem, Checkout, CheckoutItem
from apps.shop.models import Product


@login_required
def add_to_cart(request, product_id):
    cart = Cart.objects.filter(user=request.user).first()
    product = Product.objects.get(pk=product_id)

    if cart:
        cart_item = CartItem.objects.filter(cart=cart, product=product).exists()
        if cart_item:
            return redirect(request.META.get('HTTP_REFERER') or reverse('home'))
        CartItem.objects.create(cart=cart, product=product)
    else:
        cart = Cart.objects.create(user=request.user)
        CartItem.objects.create(cart=cart, product=product)

    return redirect(request.META.get('HTTP_REFERER') or reverse('home'))

@login_required
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart = cart_item.cart

    if cart.user != request.user:
        return redirect(request.META.get('HTTP_REFERER') or reverse('home'))

    cart_item.delete()

    other_items = CartItem.objects.filter(cart=cart).exists()

    if not other_items:
        cart.delete()

    return redirect(request.META.get('HTTP_REFERER') or reverse('home'))

@login_required
def cart_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_sub_total_price = cart.cart_sub_total_price
    cart_total_price = cart.cart_total_price

    context = {
        'cart_items': cart_items,
        'cart_sub_total_price': cart_sub_total_price,
        'cart_total_price': cart_total_price,
        'cart': cart,
    }

    return render(request, 'cart.html', context)

@login_required
def checkout_view(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total = cart.cart_total_price
    sub_total = cart.cart_sub_total_price

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')

        if first_name and last_name and email and phone_number and city and state and zip_code:
            checkout = Checkout.objects.create(
                user=request.user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                city=city,
                state=state,
                zip_code=zip_code,
            )
            checkout.save()

            for item in cart_items:
                CheckoutItem.objects.create(
                    checkout=checkout,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discount,
                )
            
            cart.delete()
            return redirect('home')
        else:
            return redirect('checkout')

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'total': total,
        'sub_total': sub_total,
    }

    return render(request, 'checkout.html', context)
