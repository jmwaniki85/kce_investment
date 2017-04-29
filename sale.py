from openerp import models, fields, api
from openerp.exceptions import ValidationError
import datetime

class sale_order(models.Model):
    _inherit = 'sale.order'

    schedule_ids = fields.One2many('sale.order.repayment.schedule','order_id')
    installments = fields.Integer(default = 1)

    @api.one
    def generate_schedule(self):
        installment_amount = 0.0
        schedule = []
        installment_amount = self.amount_total/self.installments
        schedule = [installment_amount for installment in range(1,self.installments + 1)]

    @api.multi
    def confirm_booking(self):
        for line in self.order_line:
            if line.product_id.product_category == 'land':
                line.product_id.status = 'reserved'
                line.product_id.sales_person = self.user_id.partner_id.id
                line.product_id.customer = self.partner_id.id
                line.product_id.sale_ok = False

    @api.one
    def cancel_booking(self):
        #raise ValidationError("This works, it's just acting up")
        for line in self.order_line:
            if line.product_id.product_category == 'land':
                line.product_id.status = 'available'
                line.product_id.sale_ok = True
        return True

    @api.model
    def scheduler_cancel_bookings(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        if setup.reservation:#do automatic cancelling of reservations only if required
            orders = self.env['sale.order'].search([('state','=','manual')])
            for order in orders:
                if datetime.datetime.strptime(str(order.date_order),'%Y-%m-%d').date() + datetime.timedelta(setup.reservation_period) > datetime.date.today():
                    order.action_cancel(context=None)

class sale_order_repayment_schedule(models.Model):
    _name = 'sale.order.repayment.schedule'

    order_id = fields.Many2one('sale.order')






