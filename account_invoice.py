from openerp import fields, api, models
from openerp.exceptions import ValidationError
from datetime import datetime

class invoice(models.Model):

    _inherit = 'account.invoice'

    schedule_ids = fields.One2many('account.invoice.repayment.schedule','invoice_id', readonly = True)
    installments = fields.Integer(default = 1)
    amount_due = fields.Float(compute = 'compute_dues')
    deposit = fields.Float()
    installment_start_date = fields.Date()
    as_at = fields.Date(compute = 'compute_dues')
    #These additional 2 fields are meant to facilitate forecasting dues
    report_as_at = fields.Date(default = fields.Date.today)
    report_amount_due = fields.Float(compute = 'compute_dues')

    @api.one
    def generate_schedule(self):
        self.schedule_ids.unlink()
        installment_amount = 0.0
        schedule = []
        installment_amount = (self.amount_total-self.deposit)/self.installments
        schedule = [installment_amount for installment in range(1,self.installments + 1)]
        due_date = self.installment_start_date#date_due
        installment = 0
        balance = self.amount_total
        repayment_schedule = self.env['account.invoice.repayment.schedule']
        for entry in schedule:
            installment += 1

            repayment_schedule.create({'invoice_id':self.id,'installment':installment, 'date_due':due_date,
                'balance':balance, 'installment_amount':entry})
            balance -= entry
            due_date = next_date(due_date)

    @api.one
    @api.depends('schedule_ids')
    def compute_dues(self):
        total = 0.0
        paid = self.amount_total - self.residual
        as_at = None
        due = 0.0
        report_due = 0.0
        for line in self.schedule_ids:
            total += line.installment_amount
            #if total < paid:
            #    line.paid = True
            #else:
            #    line.paid = False

            #calculate dues
            if datetime.strptime(line.date_due, '%Y-%m-%d') <= datetime.now():
                due += line.installment_amount
                line.due = True
                as_at = line.date_due
            #calculate dues for forecasting
            if datetime.strptime(line.date_due, '%Y-%m-%d') <= datetime.strptime(self.report_as_at,'%Y-%m-%d'):
                report_due += line.installment_amount
                #line.due = True
                #as_at = line.date_due

        if ((due-paid)>0):
            self.amount_due = due - paid #this is the true due amount
        if ((report_due-paid)>0):
            self.report_amount_due = report_due - paid
        self.as_at = as_at




    @api.multi
    def check_product_state(self):
        for line in self.invoice_line:
            if line.product_id:#avoid singleton error when no product is selected on lines
                if line.product_id.product_category == 'land':
                    line.product_id.sale_ok = False
                    line.product_id.purchase_ok = False
                    line.product_id.status = 'sold'

    @api.multi
    def add_customer_tags(self):
        customer_projects = self.partner_id.category_id
        for line in self.invoice_line:
            if line.product_id:
                if line.product_id.product_category == 'land':
                    customer_tags = self.env['res.partner.category'].search([('project_id','=',line.product_id.categ_id.id),('partner_ids','=',self.partner_id.id)])
                    if len(customer_tags)>0:
                        pass # this customer is already tagged as a member of specified product project
                    else:
                        #raise ValidationError('Tag this customer')
                        self.partner_id.category_id = [(0,0,{'name':line.product_id.categ_id.name,'active':True, 'project_id':line.product_id.categ_id.id})]


class account_invoice_repayment_schedule(models.Model):
    _name = 'account.invoice.repayment.schedule'

    invoice_id = fields.Many2one('account.invoice')
    installment = fields.Integer()
    date_due = fields.Date()
    balance = fields.Float()
    installment_amount = fields.Float()
    due = fields.Boolean(compute = 'mark_as_paid')
    paid = fields.Boolean(compute = 'mark_as_paid')

    @api.one
    @api.depends('invoice_id')
    def mark_as_paid(self):
        total = 0.0
        paid = self.invoice_id.amount_total - self.invoice_id.residual
        for line in self.invoice_id.schedule_ids:
            total += line.installment_amount
            if total < paid:
                line.paid = True
            else:
                line.paid = False

            if datetime.strptime(line.date_due, '%Y-%m-%d') <= datetime.now():
                line.due = True


def next_date(startdate_param):
        """
        This next function calculates the next month with same date. If that date is larger than available dates for the
        following month, it gets the maximum date for that month:::>>>Author:dennokorir
        """
        #we create a dictionary for months against their max days
        months_structure = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        #start calculation
        start_date = datetime.strptime(str(startdate_param),'%Y-%m-%d').date()#start_date
        current_month = start_date.month
        current_year = start_date.year
        next_month = 0
        next_year = current_year
        if current_month == 12:
            next_month = 1
            next_year += 1
        else:
            next_month = current_month + 1

        #routine to ensure we do not exceed the number of days in the next month
        end_day = start_date
        current_day = start_date.day
        if current_day < months_structure[next_month]:
            end_day = start_date.replace(month = next_month, year = next_year)
        else:
            end_day = start_date.replace(day=months_structure[next_month],month=next_month, year = next_year)#months_structure[next_month] returns max days of next month
            #end_day = start_date.replace(month=next_month)
        return end_day
