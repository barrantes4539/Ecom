from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

#Cart
def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    return render(request, "cart_summary.html", {"cart_products":cart_products})

def cart_add(request):
    # Get the cart
    cart = Cart(request)
    #Test for POST
    if request.POST.get('action') == 'post':
        # Get the data of the value product.id using the id add-cart in the product.html
        product_id = int(request.POST.get('product_id'))
        
        # Get database data
        product = get_object_or_404(Product, id=product_id)
        
        # Save to session
        cart.add(product=product)
        
        #Get cart quantity
        cart_quantity = cart.__len__()
        
        # Return response
        # response = JsonResponse({'Product Name: ': product.name})
        response = JsonResponse({'qty: ': cart_quantity})
        return response
    
def cart_delete():
    pass
def cart_update():
    pass


