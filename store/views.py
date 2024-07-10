from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
import json
from cart.cart import  Cart
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie




#ADMIN FUNCTIONS

#Categories
def admin_categories(request):
    if request.user.is_authenticated and request.user.is_superuser:
        
        categories = Category.objects.all()
        return render(request, 'admin_categories.html', {'categories':categories})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')
#Products
def admin_products(request):
    if request.user.is_authenticated and request.user.is_superuser:
        products = Product.objects.select_related('category').all()
        categories = Category.objects.all()
        return render(request, 'admin_products.html', {'products': products, 'categories':categories})
    else:
        return redirect('home')
    
@require_POST
def update_categories(request):
    # Ensure the action is 'post'
    if request.POST.get('action') == 'post':
        # Get the category ID and the category name from POST data
        category_id = int(request.POST.get('category_id'))
        category_name = request.POST.get('category_name')

        # Update the category name in the database
        try:
            category = Category.objects.get(id=category_id)
            category.name = category_name
            category.save()
            return JsonResponse({'message': f"Categoría '{category_name}' actualizada correctamente."})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'La categoría especificada no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def add_categories(request):
    # Ensure the action is 'post'
    if request.POST.get('action') == 'post':
        # Get the category ID and the category name from POST data
        new_category_name = request.POST.get('new_category_name')

        # Update the category name in the database
        try:
            # Create a new Category instance
            new_category = Category(name=new_category_name)
            # Save data in the database
            new_category.save()
            
            messages.success(request, "Categoría agregada exitosamente")
            return JsonResponse({'message': f"Categoría '{new_category_name}' agregada correctamente."})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'La categoría especificada no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def delete_categories(request):
    # Ensure the action is 'post'
    if request.POST.get('action') == 'post':
        # Get the category ID and the category name from POST data
        category_id = int(request.POST.get('category_id'))
        category_name = request.POST.get('category_name')

        try:
            # Find the category by ID and delete it
            category = Category.objects.get(id=category_id)
            category_name = category.name  # Store category name for response message
            category.delete()
            
            return JsonResponse({'message': f"Categoría '{category_name}' eliminada correctamente."})
        except Category.DoesNotExist:
            return JsonResponse({'error': 'La categoría especificada no existe.'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)

@require_POST
def update_products(request):
    # Ensure that the request is POST
    if request.POST.get('action') == 'post':
        # Get data
        product_id = int(request.POST.get('product_id'))
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_category_id = request.POST.get('product_category')  # Obtener el ID de la categoría
        product_image = request.FILES.get('product_image')  # Obtener la imagen del producto
        
        try:
            # Obtener el producto de la base de datos
            product = Product.objects.get(id=product_id)
            product.name = product_name
            product.sale_price = product_price
            
            # Actualizar la categoría solo si se proporcionó un ID válido y no es 'undefined'
            if product_category_id and product_category_id != 'undefined':
                product.category_id = int(product_category_id)

            # Actualizar la imagen solo si se proporcionó
            if product_image:
                product.image = product_image
            
            # Guardar el producto actualizado
            product.save()
            
            return JsonResponse({'message': f"Producto '{product_name}' actualizado correctamente."})
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'El producto especificado no existe.'}, status=404)
        
        except ValueError:
            return JsonResponse({'error': 'El ID de categoría proporcionado no es válido.'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Solicitud inválida'}, status=400)

@ensure_csrf_cookie
@require_POST
def add_products(request):
    # Verificar que la acción sea un POST
    if request.method == 'POST':
        new_product_name = request.POST.get('new_product_name')
        new_product_price = request.POST.get('new_product_price')
        new_product_category_id = request.POST.get('new_product_category')
        new_product_description = request.POST.get('new_product_description')
        new_product_img = request.FILES.get('new_product_img')

        try:
            # Crear una instancia de Product con los datos recibidos
            new_product = Product(
                name=new_product_name,
                sale_price=new_product_price,
                category_id=new_product_category_id,  # Usar category_id si es una clave externa
                description=new_product_description,
                image=new_product_img
            )
            new_product.save()

            messages.success(request, "Producto agregado exitosamente")
            return JsonResponse({'message': f"Producto '{new_product_name}' agregado correctamente."})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    # Devolver un error si la solicitud no es un POST
    return JsonResponse({'error': 'Invalid request'}, status=400)




#END ADMIN FUNCIONS

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
        
        # Look up the product filtered by category
        products = Product.objects.filter(category=category)
        
        return render(request, 'category.html', {'products':products,'category':category})
    except:
        messages.success(request, ('La categoría no existe.'))
        return redirect('home')
    

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                # Retrieve the profile for the logged-in user
                current_user_profile = Profile.objects.get(user=user)
                
                # Get the saved cart (old_cart) from database
                saved_cart = current_user_profile.old_cart
                
                if saved_cart:
                    try:
                        # Convert database string to Python dictionary
                        converted_cart = json.loads(saved_cart)
                        
                        # Add the loaded cart items to the current session cart
                        cart = Cart(request)
                        for key, value in converted_cart.items():
                            cart.db_add(product=key, quantity=value)
                        
                        messages.success(request, "Has iniciado sesión")
                    except json.JSONDecodeError:
                        messages.error(request, "Error al cargar el carrito guardado")
                else:
                    messages.info(request, "Agrega productos a tu carrito!!")
                
                return redirect('home')
            
            except Profile.DoesNotExist:
                messages.error(request, "No se encontró el perfil asociado con su cuenta")
                return redirect('login')
            
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return redirect('login')
    
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
            return redirect('user_info')
        else:
            # Collect form errors and display them
            error_messages = form.errors.as_data()
            for field, errors in error_messages.items():
                for error in errors:
                    messages.error(request, f"{field}: {error.message}")

            messages.error(request, "Ha habido un error registrando su cuenta, intente de nuevo")
            return redirect('register')

    else:    
        return render(request, 'register.html', {'form':form})

# User
def user_info(request):
    if not request.user.is_authenticated:
        return redirect('login')
    #Get current User
    current_user = Profile.objects.get(user__id=request.user.id)
    #Get current User's Shipping Info
    shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
    #Get original User Form
    form = UserInfoForm(request.POST or None, instance=current_user)
    #Get User Shipping Form
    shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
    if form.is_valid() or shipping_form.is_valid():
        #Save Original form
        form.save()
        #Save shipping form
        shipping_form.save()
        messages.success(request, ("Tu información ha sido actualizada exitosamente!!"))
        return redirect('home')
    return render(request, 'user_info.html', {'form': form, 'shipping_form': shipping_form})

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

        
        


