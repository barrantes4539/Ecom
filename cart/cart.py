from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        
        cart = self.session.get('session_key')
        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        # Make sure cart is available in all pages
        self.cart = cart
    
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'2':3, '4':1} to {"2":3, "4":1}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        
    # Function to add product in cart
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True
        
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'2':3, '4':1} to {"2":3, "4":1}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        
    # Function to see quantity of products in the car 
    def __len__(self):
        return len(self.cart)
    
    # Get the cart products
    def get_products(self):
        # Get ids from cart
        products_ids = self.cart.keys()
        # Use ids to lookup products in database model
        products = Product.objects.filter(id__in=products_ids)
        # Return the lookup products
        return products

    def get_quants(self):
        quantities = self.cart
        return quantities
    
    # Function to update product quantity
    def update(self, product, quantity):
        try:
            product_id = str(product)
            product_qty = int(quantity)
            # Get cart
            ourcart = self.cart
            # Update dict
            ourcart[product_id] = product_qty
            # Update session
            self.session.modified = True
            if self.request.user.is_authenticated:
                # Get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # Convert {'2':3, '4':1} to {"2":3, "4":1}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to profile model
                current_user.update(old_cart=str(carty))
            thing = self.cart
            return thing
        except Exception as e:
            # Manejo de la excepción
            print("Error:", e)
            return None  # o cualquier otro manejo de error que desees hacer
    
    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.session.modified = True
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert {'2':3, '4':1} to {"2":3, "4":1}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to profile model
            current_user.update(old_cart=str(carty))
        
    def cart_total(self):
        '''
        This is how actually elemets are seing in the dictionary
        {'4':3, '2':4} '4' is the id and 3 is the quantity (investigar comando para depurar sesion en terminal de python)
        '''
        #Get products ids
        product_ids = self.cart.keys()
        #Lookup those keys in our products database models
        products = Product.objects.filter(id__in=product_ids)
        #Get quantities
        quantities = self.cart
        #start counting at 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into an int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.sale_price * value)
        return total

            
            
            