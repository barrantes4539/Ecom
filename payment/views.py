from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib import messages
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product

def process_order(request):
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        #Get Billing Info from the last page
        payment_form = PaymentForm(request.POST or None)
        
        #Get Shipping Session Data
        my_shipping = request.session.get('my_shipping')
        
        #Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
    
        #Create Shipping Address from session Info
        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals
        
        #Create an Order
        if request.user.is_authenticated:
            
            #Logged in
            user = request.user
            
            #Create Order
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            '''Add Order Items'''
            #Get the Order ID
            order_id = create_order.pk
            
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                price = product.sale_price
                #Get quantity of each product
                for key,value in quantities().items():
                    if int(key) == product.id:
                        '''Create Order Item'''
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,quantity=value,price=price)
                        create_order_item.save()
                        
            messages.success(request, "Order Placed!")
            return redirect('home')
        else:
            #Create Order as guest
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            '''Add Order Items as guest'''
            #Get the Order ID
            order_id = create_order.pk
            
            for product in cart_products():
                #Get product ID
                product_id = product.id
                #Get product price
                price = product.sale_price
                #Get quantity of each product
                for key,value in quantities().items():
                    if int(key) == product.id:
                        '''Create Order Item as guest'''
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,user=user,quantity=value,price=price)
                        create_order_item.save()
                        
            messages.success(request, "Order Placed!")
            return redirect('home')
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')


def billing_info(request):
    
    if request.POST:
        # Get the cart
        cart = Cart(request)
        cart_products = cart.get_products
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        #Create a session with Shipping Info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        #Check to see if user is Log In
        if request.user.is_authenticated:
            #Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals,"shipping_info":request.POST, "billing_form": billing_form})
        else:
            #Get the Billing Form
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_info":request.POST, "billing_form": billing_form})
        
    else:
        messages.success(request, "Acceso Denegado")
        return redirect('home')


def checkout(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_products
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        #Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        #Checkout logged as user 
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        #Shipping Form
        shipping_form = ShippingForm(request.POST or None)
        # Checkout as guest
        return render(request, "payment/checkout.html", {"cart_products": cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    

def payment_success(request):
    return render(request, "payment/payment_success.html", {})