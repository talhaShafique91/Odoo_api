import pandas as pd
from app.odoo_client import OdooClient

class OrderProcessor:
    def __init__(self, odoo_client, csv_path):
        self.odoo_client = odoo_client
        self.csv_path = csv_path

    def check_or_create_partner(self, seller_id, seller_name, seller_phone):
        partner_id = self.odoo_client.search_partner(seller_name)
        if not partner_id:
            partner_data = {
                'name': seller_name,
                'phone': seller_phone,
                'id': seller_id,
            }
            partner_id = self.odoo_client.create_partner(partner_data)
        else:
            partner_id = partner_id[0]

        return partner_id
    

    def check_or_create_product(self, sku_id, product_name):
        product_id = self.odoo_client.search_product(product_name)
        if not product_id:
            product_data = {
                'name': product_name,
                'default_code': sku_id,
            }
            product_id = self.odoo_client.create_product(product_data)
        else:
            product_id = product_id[0]

        return product_id
    
    
    def check_or_create_or_update_order(self, order_id, order_date, partner_id, product_id, ordered_qty, order_price):
        existing_order_id = self.odoo_client.search_order(order_id)

        if not existing_order_id:
            order_data = {
                'partner_id': partner_id,
                'name': order_id,
                'date_order': order_date,
                'order_line': [(0, 0, {
                    'product_id': product_id,
                    'product_uom_qty': ordered_qty,
                    'price_unit': order_price,
                })],
            }
            order_id = self.odoo_client.create_order(order_data)
            self.odoo_client.confirm_order(order_id)
        else:
            order_line_id = self.odoo_client.search_order_line(existing_order_id[0], product_id)
            if order_line_id:
                self.odoo_client.update_order_line(order_line_id[0], {
                    'product_id': product_id,
                    'product_uom_qty': ordered_qty,
                    'price_unit': order_price,
                })
            else:
                self.odoo_client.create_order_line({
                    'order_id': existing_order_id[0],
                    'product_id': product_id,
                    'product_uom_qty': ordered_qty,
                    'price_unit': order_price,
                })
            order_state = self.odoo_client.search_order_state(existing_order_id)
            if order_state in ['draft', 'sent']:
                self.odoo_client.confirm_order(existing_order_id[0])

        return order_id
    

    def process_order(self, row):
        partner_id = self.check_or_create_partner(row['Seller ID'], row['Seller Name'], row['Seller Mobile Number'])
        product_id = self.check_or_create_product(row['sku_id'], row['Product Name'])
        order_id = self.check_or_create_or_update_order(row['Order ID'], row['Order Date'], partner_id, product_id, row['Ordered Qty'], row['Order Price'])

        return order_id
    

    def process_orders(self):
        df = pd.read_csv(self.csv_path)
        for _, row in df.iterrows():
            try:
                self.process_order(row)
                print(f"Processed Order ID: {row['Order ID']}")
            except Exception as e:
                print(f"Failed to process Order ID: {row['Order ID']} due to {e}")