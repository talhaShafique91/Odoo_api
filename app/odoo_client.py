import xmlrpc.client

class OdooClient:
    def __init__(self, url, db, username, password):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        self.uid = self.authenticate()
        self.models = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/object')

    def authenticate(self):
        common = xmlrpc.client.ServerProxy(f'{self.url}/xmlrpc/2/common')
        return common.authenticate(self.db, self.username, 
                                   self.password, {})
    

    def search_partner(self, seller_name):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                        'res.partner', 'search',
                                        [[['name', '=', seller_name]]])
        

    def create_partner(self, seller_data):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                       'res.partner', 'create',
                                       [seller_data])


    def search_product(self, product_name):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                        'product.product', 'search',
                                        [[['name', '=', product_name]]])
    

    def create_product(self, product_data):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                       'product.product', 'create',
                                       [product_data])


    def search_order(self, order_id):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      'sale.order', 'search',
                                      [[['name', '=', order_id]]])
    
    
    def search_order_state(self, existing_order_id):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      'sale.order', 'read',
                                      [existing_order_id, ['state']])[0]['state']


    def create_order(self, order_data):
        return self.models.execute_kw(self.db, self.uid, self.password, 
                                      'sale.order', 'create', [order_data])
    

    def confirm_order(self, order_id):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      'sale.order', 'action_confirm', [[order_id]])
    

    def search_order_line(self, order_id, product_id):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      'sale.order.line', 'search',
                                      [[['order_id', '=', order_id], ['product_id', '=', product_id]]])
    
    def update_order_line(self, order_line_id, update_data):
        return self.models.execute_kw(self.db, self.uid, self.password,
                                      'sale.order.line', 'write',
                                      [[order_line_id], update_data])

    def create_order_line(self, order_line_data):
        return self.models.execute_kw(self.db, self.uid, self.password, 
                                      'sale.order.line', 'create', 
                                      [order_line_data])