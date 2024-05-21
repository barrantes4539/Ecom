from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


def cart_summary(request):
    if not request.user.is_authenticated:
        return redirect('login')

    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, "cart_summary.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals})

def cart_add(request):
    # Ensure the request is a POST request and the action is 'post'
    if request.method == "POST" and request.POST.get('action') == 'post':
        if not request.user.is_authenticated:
            return JsonResponse({'unauthorized': 'User not authenticated'}, status=401)

        # Get the cart
        cart = Cart(request)
        
        # Get the product ID and quantity from the POST data
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        # Fetch the product from the database
        product = get_object_or_404(Product, id=product_id)
        
        # Add the product to the cart
        cart.add(product=product, quantity=product_qty)
        
        # Get the total quantity of items in the cart
        cart_quantity = cart.__len__()
        
        # Return a JSON response with the updated cart quantity
        return JsonResponse({'qty': cart_quantity})
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') =='post':
        product_id = int(request.POST.get('product_id'))
        
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        return response

def cart_update(request):

    if not request.method == 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Expected POST.'})

    # Extract product ID and quantity from request
    product_id = request.POST.get('product_id')
    product_qty = int(request.POST.get('product_qty'))

    try:
        # Get the cart
        cart = Cart(request)

        # Get the product
        #product = get_object_or_404(Product, id=product_id)
        # Update cart item quantity
        cart.update(product=product_id, quantity=product_qty)
        response = JsonResponse({'qty':product_qty})
        return response
        #return redirect('cart_summary')

    except (Product.DoesNotExist, ValueError):
        return JsonResponse({'success': False, 'message': 'Error updating cart item.'})


