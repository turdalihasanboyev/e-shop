from django.shortcuts import render, redirect

from .models import Product, Review


def shop_view(request):
    q = request.GET.get('q')

    products = Product.objects.all()

    if q:
        products = products.filter(name__icontains=q)

    return render(request, 'shop.html', {'products': products})

def product_detail_view(request, product_slug):
    product = Product.objects.get(slug=product_slug)

    product.views += 1
    product.save()

    reviews = Review.objects.filter(product=product).order_by('-id')
    related_products = Product.objects.filter(category=product.category).exclude(pk=product.pk)

    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        review = request.POST.get('review')

        if name and email and review:
            Review.objects.create(
                product=product,
                user=request.user,
                name=name,
                email=email,
                review=review,
            )
            return redirect(product.get_absolute_url())
        else:
            return redirect(product.get_absolute_url())

    context = {
        'product': product,
        'reviews': reviews,
        'related_products': related_products,
    }

    return render(request, 'detail.html', context)
