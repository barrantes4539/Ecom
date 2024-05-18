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


