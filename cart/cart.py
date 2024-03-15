from store.models import Product, Profile


class Cart():
    def __init__(self,request):
        self.session = request.session
        # Ge Request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # if the user is new, no sesion key! Create one
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {} 


        # Make sure cart is available on all pages of the site
        self.cart = cart


    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        # logic
        if product_id in self.cart:
            pass
        else:
            #self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
        self.session.modified = True

        # Deal with Logged In User
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # Convert
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # Get product IDS
        product_ids = self.cart.keys()
        # lookup those keys in our database model
        products = Product.objects.filter(id__in=product_ids)
        # Get quantities
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            # Convert key string into int , to do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)    
            return total 


    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()
        # Use ids to lookup products in databse model
        products = Product.objects.filter(id__in=product_ids)
        # Return looked up products
        return products
        
    def get_quants(self):
        quantities = self.cart
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get Cart
        ourcart = self.cart
        # Update Dictionary/cart
        ourcart[product_id] = product_qty

        self.session.modified = True

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)
        # Delete from Cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        
        