from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

#Cart
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    return render(request, "cart_summary.html", {"cart_products":cart_products, "quantities":quantities})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    #Test for POST
    if request.POST.get('action') == 'post':
        # Get the data of the value product.id using the id add-cart in the product.html
        product_id = int(request.POST.get('product_id'))
        
        # Get the quantity
        product_qty = int(request.POST.get('product_qty'))
        
        # Get database data
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product, quantity=product_qty)
        
        #Get cart quantity
        cart_quantity = cart.__len__()
        
        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        return response
    
def cart_delete():
    pass

def cart_update(request):
    """
    Updates the quantity of a product in the user's cart.

    Expects a POST request with the following data:
        - product_id: Integer representing the product ID.
        - quantity: Integer representing the desired quantity for the product.

    Returns a JSON response with:
        - success: Boolean indicating update success.
        - message: String message regarding the update.
        - cart_total: Float representing the updated cart total (optional).
    """
    if not request.method == 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid request method. Expected POST.'})

    # Extract product ID and quantity from request
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity'))

    # Error handling - validate data
    if not product_id or quantity < 0:
        return JsonResponse({'success': False, 'message': 'Invalid product ID or quantity.'})

    try:
        # Get the cart
        cart = Cart(request)

        # Get the product
        product = get_object_or_404(Product, id=product_id)
        

        # Update cart item quantity
        cart.update(product, quantity)

        # Calculate updated cart total (optional)
        cart_total = cart.get_total_price() if hasattr(cart, 'get_total_price') else None

        return JsonResponse({'success': True, 'message': 'Cart updated successfully.', 'cart_total': cart_total})

    except (Product.DoesNotExist, ValueError):
        return JsonResponse({'success': False, 'message': 'Error updating cart item.'})


