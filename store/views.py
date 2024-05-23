from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms


#Store
def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})

def category(request, cat):
    #Grab the category from the url
    print(f"Received category: {cat}")
    try:
        # Look up the category
        category = Category.objects.get(name=cat)
        print(f"URL category: {category}")
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products,'category':category})
    except:
        messages.success(request, ('La categoría no existe.'))
        return redirect('home')
    
#Authentication
def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, ("Has iniciado Sesión"))
            return redirect('home')
        else:
            messages.success(request, ("Ha habido un error, intente de nuevo"))
            return redirect('login')
    else:
        return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Has cerrado sesión"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Has sido registrado exitosamente!!"))
            return redirect('home')
        else:
            messages.success(request, ("Ha habido un error registrando su cuenta, intente de nuevo"))
            return redirect('register')
    else:    
        return render(request, 'register.html', {'form':form})

# User
def user_info(request):
    if not request.user.is_authenticated:
        return redirect('login')
    current_user = Profile.objects.get(user__id=request.user.id)
    form = UserInfoForm(request.POST or None, instance=current_user)
    if form.is_valid():
        form.save()
        messages.success(request, ("Tu información ha sido actualizada exitosamente!!"))
        return redirect('user_profile')
    return render(request, 'user_info.html', {'form': form})

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ("Tu perfil ha sido actualizado exitosamente!!"))
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, 'user_profile.html', {'user_form': user_form})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Has cambiado la contraseña exitosamente")
                login(request, current_user)
                return redirect('user_profile')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.success(request, ("Debes iniciar sesión primero"))
        return redirect('login')
    


