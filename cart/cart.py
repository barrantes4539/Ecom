from store.models import Product

class Cart():
    def __init__(self, request) -> None:
        self.session = request.session
        
        # Get the current session if it exists
        cart = self.session.get('session_key')
        
        # If the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        # Make sure cart is available in all pages
        self.cart = cart
    
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
        product_id = str(product.id)

        # Check if product exists in the cart
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity  # Update quantity
        else:
        # If product doesn't exist, consider raising an exception or handling it differently
            raise ValueError(f"Product with ID {product_id} not found in cart.")

        self.session.modified = True  # Mark session as modified
        
    # Function to calculate total price of all items in cart
    def get_total_price(self):
        total_price = 0
        for item in self.cart.items():
            product_id, item_data = item
            product = Product.objects.get(pk=product_id)  # Get product object using ID
            quantity = int(item_data['quantity'])
            price = int(product.price)
            total_price += quantity * price
        return total_price
            
            
            