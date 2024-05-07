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
        
    def add(self, product):
        product_id = str(product.id)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = {'price':str(product.price)}
        self.session.modified = True
        