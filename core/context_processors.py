from products.models import Category
from core.models import NavbarCategory


def navbar_categories(request):
    """
    Context processor to inject navbar categories and all categories globally
    """
    nav_categories = NavbarCategory.objects.all()[:5]
    all_categories = Category.objects.all()
    
    return {
        'nav_categories': nav_categories,
        'all_categories': all_categories,
    }
