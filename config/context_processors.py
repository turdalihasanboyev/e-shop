from apps.shop.models import Category

def custom_context_processors(request):
    # Add custom context processors here
    categories = Category.objects.all()
    context = {'categories': categories}
    return context