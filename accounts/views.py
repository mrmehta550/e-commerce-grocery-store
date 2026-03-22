from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login,authenticate,logout

def register_view(request):
    form = RegisterForm(request.POST or None)
    
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('shop')
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('shop')
            else:
                form.add_error(None, "Invalid username or password")

   
    return render(request, 'login.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('login')