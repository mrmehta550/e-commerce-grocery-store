from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.views.generic import TemplateView
from orders.models import Order
from accounts.models import Address

def register_view(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('shop')
    
    return render(request, 'register.html', {'form': form})


@csrf_protect
def login_view(request):
    form = LoginForm(request.POST or None)
    next_url = request.GET.get('next') or request.POST.get('next') or 'shop'

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', {'form': form, 'next': next_url})
    
def logout_view(request):
    logout(request)
    return redirect('login')

class MyAccountView(TemplateView):
    template_name = "my-account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        context['orders'] = Order.objects.filter(user=user).order_by('-created_at')[:5]
        context['addresses'] = Address.objects.filter(user=user)

        return context