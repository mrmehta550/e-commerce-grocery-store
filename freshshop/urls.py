
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cart/', include('cart.urls')),
    path('shop/', include('products.urls')),
    path('api/', include('api.urls')),
    path('accounts/', include('accounts.urls')),
    path('provider/', include('providers.urls')),
    path('dashboard/', RedirectView.as_view(pattern_name='provider_dashboard', permanent=False), name='dashboard'),

] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)