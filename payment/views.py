from django.shortcuts import render, get_object_or_404, redirect
from cart.cart import Cart
from django.http import JsonResponse
from django.contrib import messages
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product, Profile
import datetime


#Admin
def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        
        #Get the order
        order = Order.objects.get(id=pk)
        #Get the order items
        items = OrderItem.objects.filter(order=pk)
        
        if request.POST:
            status = request.POST['shipping_status'] #True or False
            if status == "true":
                #Get the order
                order = Order.objects.filter(id=pk)
                #Update the status
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now) #shipped and date_shipped come from payment/models
            else:
                #Get the order
                order = Order.objects.filter(id=pk)
                #Update the status
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        
        return render(request, "payment/orders.html", {"order":order, "items":items})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status'] #True or False
            num = request.POST['num']
            #Get the order
            order = Order.objects.filter(id=num)
            
            #Grab Date and Time
            now = datetime.datetime.now()
            #Update Order
            order.update(shipped=True, date_shipped=now) #shipped and date_shipped come from payment/models

            #Message and Redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        
        return render(request, "payment/not_shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status'] #True or False
            num = request.POST['num']
            
            #Get the order
            order = Order.objects.filter(id=num)
            #Grab Date and Time
            now = datetime.datetime.now()
            #Update Order
            order.update(shipped=False) #shipped and date_shipped come from payment/models

            #Message and Redirect
            messages.success(request, "Shipping Status Updated")
            return redirect('home')
        
        return render(request, "payment/shipped_dash.html", {"orders":orders})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')

#Customer
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
        
        #Create an Order8
        if request.user.is_authenticated:
            
            #Logged in
            user = request.user
            
            '''Create Order'''
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
            
            '''Delete our cart from cookies'''
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
                    
            '''Delete our cart from Database (old_cart field)'''
            current_user = Profile.objects.filter(user__id=request.user.id)
            
            '''Delete our cart from Database (old_cart field)'''
            current_user.update(old_cart="")
            
                        
            messages.success(request, "Order Placed!")
            return redirect('home')
        else:
            #Create Order as guest
            #Get the Order ID
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            #Add Order Items as guest
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
            
            '''Delete our cart'''
            for key in list(request.session.keys()):
                if key == "session_key":
                    # Delete the key
                    del request.session[key]
                        
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