from django.views.generic import TemplateView
from .models import *


class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['slider'] = Slider.objects.all()
        context['categories'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['top_featured'] = Product.objects.filter(tag='top')
        context['best_seller'] = Product.objects.filter(tag='best')
        context['banners'] = Banner.objects.all()[:5]
        context['blogs'] = Blog.objects.all()[:6]
        context['instagram'] = InstagramImage.objects.all()[:1]
        
        return context
    
    
class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["about"] = About.objects.first()
            context["services"] = Service.objects.all()
            context["teams"] = Team.objects.all()
            return context
        
class CartView(TemplateView):
    template_name = 'cart.html'
    
class CheckoutView(TemplateView):
    template_name = 'checkout.html'

class ContactView(TemplateView):
    template_name = 'contact-us.html'
    
class GalleryView(TemplateView):
    template_name = 'gallery.html'

class AccountView(TemplateView):
    template_name = 'my-account.html'
    
class ShopDetail(TemplateView):
    template_name = 'shop-detail.html'
    
class ShopView(TemplateView):
    template_name = 'shop.html'
    
class WishlistView(TemplateView):
    template_name = 'wishlist.html'
