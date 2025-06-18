from apps.shop.models import Category
from apps.checkout.models import CartItem

def custom_context_processors(request):
    # Add custom context processors here
    categories = Category.objects.all()
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    context = {'categories': categories, 'cart_items_count': cart_items_count}
    return context