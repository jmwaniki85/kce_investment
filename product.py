from openerp import models, api, fields
from openerp.exceptions import ValidationError

#Extenstions to include fields specific for land transactions
#on product model

class product(models.Model):
    _inherit = 'product.template'

    total_acreage = fields.Float()
    title_deed_no = fields.Char()
    product_category = fields.Selection([('land',"Land"),('housing',"Housing"),('item',"Item")], default = "item", string = 'Product Category')
    ballot = fields.Char()
    sold = fields.Boolean(compute = 'check_if_sold')
    status = fields.Selection([('available',"Available"),('reserved',"Reserved"),('sold',"Sold")], default = 'available')
    sales_person = fields.Many2one('res.partner', string = "Reserved By")
    customer = fields.Many2one('res.partner', domain = [('customer','=',True)], string = "Purchased By")
    sale_order_line_product_ids = fields.One2many('sale.order.line','product_id')

    @api.onchange('product_category')
    def check_purchasable(self):
        if self.product_category == 'land':
            setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
            if not setup.land_asset_account:
                raise ValidationError('Land Asset Account must have a value in Investment > Configuration > General Setup')
            else:

                    self.property_stock_account_input = setup.land_input_account.id
                    self.property_stock_account_output = setup.land_output_account.id
                    self.property_account_income = setup.land_income_account.id
                    self.property_account_expense = setup.land_expense_account.id
                    self.valuation = 'real_time'
                    self.cost_method = 'real'
                    self.type = 'product'
    @api.one
    @api.depends('sale_order_line_product_ids')
    def check_if_sold(self):
        if self.product_category == 'land':
            if len(self.sale_order_line_product_ids)>0:
                self.sold = True
                self.sale_ok = False


    @api.model
    def cancel_all_reservations(self):
        product = self.env['product.template'].search([])
        product.write({'status':'available','sale_ok':True})

    @api.onchange('title_deed_no')
    def suffix_plot_name(self):
        if self.name:
            self.name = self.name+'['+self.title_deed_no+']'
