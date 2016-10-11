from openerp import models, fields

class sale_subscription_improvements(models.Model):
    _inherit = ['sale.subscription']
    
    on_site_product = fields.Many2one('product.product', string="Travel Product", index=True, help="Product that will be used to compute the price of the travel when the work is done on site.")
    on_site_invoice_by_km = fields.Boolean(string="Invoice by km", help="True: price = km * on site product public price, False: price = on site product public price")
    on_site_distance_in_km = fields.Float("Distance in km")