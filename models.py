# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import ValidationError

class investor_registration(models.Model):
    _name = 'sale.investor.registration'

    no = fields.Char()
    name = fields.Char(string = 'Other Names')
    address = fields.Char(string = 'Address')
    city = fields.Char()
    phone_no = fields.Char(string = 'Phone No.', required = True)
    mobile_no = fields.Char()
    email = fields.Char(string = 'Email')
    registration_date = fields.Date(default = fields.Date.today)
    state = fields.Selection([('open',"Open"),('pending',"Pending"),('approved',"Approved"),('rejected',"Rejected")],default = 'open')
    date_of_birth = fields.Date(string = 'Date of Birth')
    home_address = fields.Char()
    location = fields.Char(string = 'SUB-COUNTY (Gichigo)')
    sublocation = fields.Char(string = 'SUB-LOCATION (Ituura)')
    district = fields.Char()
    idno = fields.Char(required = True)
    passportno = fields.Char()
    marital_status = fields.Selection([('single','Single'),('married','Married')])
    gender = fields.Selection([('male','Male'),('female','Female')])
    monthly_contribution = fields.Float()
    dividend_amount = fields.Float()
    occupation = fields.Char()
    designation = fields.Selection([('mr',"MR"),('mrs',"Mrs"),('miss',"Miss")])
    contact_person = fields.Char()
    contact_person_phone_no = fields.Char()
    contact_person_relation = fields.Selection([('kin','Kin'),('relative','Relative'),('friend','Friend')])
    recruited_by = fields.Char()
    sales_person = fields.Many2one('res.partner', string = 'Recruited By')
    approved_by = fields.Char()
    bank_name = fields.Char()
    bank_account_no = fields.Char()
    investor_pin = fields.Char()
    image = fields.Binary("Image",help = "Member Image")
    created = fields.Boolean()
    investor_type = fields.Selection([('individual',"Individual"),('group',"Group"),('company',"Company")])
    company_registration = fields.Char(string = 'Company/Group Registration')
    company_registration_date = fields.Date(string = 'Company/Group Registration Date')
    investor_group_ids = fields.One2many('sale.investment.invetor.group','investor_app_id')
    next_of_kin_ids = fields.One2many('next.of.kin','investor_app_id')
    sir_name = fields.Char()
    clan = fields.Many2one('sale.investment.clan', string = 'Clan(Muhiriga)')
    county = fields.Many2one('sale.investment.county')
    estate_village = fields.Char(string = 'Estate/Village(Gichagi)')
    family = fields.Char(string = 'Family(Mbari)')


    @api.one
    def create_investor(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        sequence = self.env['ir.sequence'].search([('id','=',setup.investor_nos.id)])
        investor_no = sequence.next_by_id(sequence.id, context = None)

        investor = self.env['res.partner'].create({'name':self.name,'investor':True,'phone':self.phone_no,'mobile':self.mobile_no,
            'email':self.email,'street2':self.address,'city':self.city,'customer':True, 'investor_no':investor_no,'dob':self.date_of_birth,
            'idno':self.idno,'passport_no':self.passportno,'investor_pin':self.investor_pin,'marital_status':self.marital_status,'gender':self.gender,
            'occupation':self.occupation})

        #write ids to next of kin table to transfer view to member table
        for kin in self.next_of_kin_ids:
            kin.investor_id = investor.id

        self.created = True

    @api.one
    def create_kcit(self):
        self.is_kcit = True


    @api.one
    @api.onchange('no')
    def get_sequence(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        sequence = self.env['ir.sequence'].search([('id','=',setup.investor_application_nos.id)])
        self.no = sequence.next_by_id(sequence.id, context = None)

class investment_group(models.Model):
    _name = 'sale.investment.invetor.group'

    name = fields.Char()
    idno = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    investor_app_id = fields.Many2one('sale.investor.registration')
    investor_id = fields.Many2one('res.partner')

class investor_closure(models.Model):
    _name = 'sale.investment.investor.closure'
    no = fields.Char()
    investor_no = fields.Many2one('res.partner' ,store = True , domain = [('investor','=',True)])
    image = fields.Binary(help = 'Member Image')
    closing_date = fields.Date()
    state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")],default='open')
    closed = fields.Boolean(default = False)
    closure_type = fields.Selection([('dismissal',"Summary Dismissal")])
    remarks = fields.Text()

    @api.one
    @api.onchange('no')
    def get_sequence(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        sequence = self.env['ir.sequence'].search([('id','=',setup.investor_closure_nos.id)])
        self.no = sequence.next_by_id(sequence.id, context = None)

    @api.one
    def deactivate(self):
        investor = self.env['res.partner'].search([('id','=',self.investor_no.id)])
        investor.ative = False
        self.Closed = True

class investor_activation(models.Model):
    _name = 'sale.investment.investor.activation'
    no = fields.Char()
    investor_no = fields.Many2one('res.partner', store = True ,domain = [('investor','=',True)])
    activation_date = fields.Date()
    state = fields.Selection([('open',"Open"),('pending',"Pending Approval"),('approved',"Approved"),('rejected',"Rejected")],default='open')
    activated = fields.Boolean(default = False)

    @api.one
    def activate(self):
        investor = self.env['res.partner'].search([('id','=',self.investor_no.id)])
        investor.ative = True
        self.Closed = True

    @api.one
    @api.onchange('no')
    def get_sequence(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        sequence = self.env['ir.sequence'].search([('id','=',setup.investor_activation_nos.id)])
        self.no = sequence.next_by_id(sequence.id, context = None)

class project_costing(models.Model):
    _name = 'investment.project.costing.header'

    no = fields.Char()
    name = fields.Char(required = True)
    description = fields.Char()
    date = fields.Date(default = fields.Date.today())
    title_deed_no = fields.Char()
    costing_from = fields.Selection([('quotation',"Quotation"),('invoice',"Invoice")], default = 'quotation')
    vendor = fields.Many2one('res.partner')
    vendor_quotation = fields.Many2one('purchase.order')
    vendor_invoice = fields.Many2one('purchase.order')
    purchase_cost = fields.Float(compute = 'compute_purchase_cost')
    total_acreage = fields.Float()
    allocation_to_ammenities = fields.Float()
    useful_acreage = fields.Float()
    allocated = fields.Float(compute = 'compute_allocation')
    unallocated = fields.Float(compute = 'compute_allocation')
    user_id = fields.Many2one('res.users',default=lambda self: self.env.user)
    profit_margin = fields.Float(string = "% Profit Margin")
    state = fields.Selection([('draft',"Draft"),('ready',"Ready")], default = 'draft')
    posted = fields.Boolean()
    line_ids = fields.One2many('investment.project.costing.lines', 'header_id','Project Costing', copy = True)
    costing_setup_ids = fields.One2many('investment.land.transaction.costs.local','project_id')
    percentage_allocation = fields.Float(compute = 'compute_allocation')
    total_land_cost = fields.Float()
    total_overheads = fields.Float()
    total_margin = fields.Float()
    total_price = fields.Float()
    overhead_summary_ids = fields.One2many('sale.investment.overheads.summary','header_id')

    @api.onchange('total_acreage','allocation_to_ammenities')
    def compute_acreage(self):
        if self.total_acreage>0:
            self.useful_acreage = self.total_acreage - self.allocation_to_ammenities
        else:
            self.useful_acreage = 0

    @api.one
    @api.depends('line_ids')
    def compute_allocation(self):
        '''
        total = 0
        for line in self.line_ids:
            total += line.allocation_percentage
        self.percentage_allocation = total
        '''
        if self.useful_acreage > 0:
            total = 0.0
            total_allocated = 0.0
            total_unallocated = self.useful_acreage
            for line in self.line_ids:
                #total += line.acreage_to_use
                total_allocated += (line.acreage_to_use//line.size_of_plots)*line.size_of_plots

            self.percentage_allocation = (total_allocated/self.useful_acreage)*100
            self.allocated = total_allocated
            self.unallocated = self.useful_acreage - total_allocated

    @api.one
    @api.depends('costing_from','vendor_quotation','vendor_invoice')
    def compute_purchase_cost(self):
        if self.costing_from == 'quotation':
            order = self.env['purchase.order'].search([('id','=',self.vendor_quotation.id)])
        else:
            order = self.env['purchase.order'].search([('id','=',self.vendor_invoice.id)])

        self.purchase_cost = order.amount_total
        self.vendor = order.partner_id
        self.total_acreage = order.order_line.product_id.total_acreage
        self.title_deed_no = order.order_line.product_id.title_deed_no


    @api.one
    @api.constrains('percentage_allocation')
    def check_allocations(self):
        if self.percentage_allocation>100:
            raise ValidationError("Your allocations exceed 100%")


    @api.one
    @api.onchange('no')
    def get_sequence(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        sequence = self.env['ir.sequence'].search([('id','=',setup.project_nos.id)])
        self.no = sequence.next_by_id(sequence.id, context = None)

    @api.one
    def mark_as_ready(self):
        self.overhead_summary_ids.unlink()
        transactions = self.env['investment.land.transactions'].search([])
        for transaction in transactions:
            code = ''
            description = ''
            fee_charged = 0.0
            vat = 0.0
            total_cost = 0.0
            for line in self.line_ids:
                for overhead in line.line_ids:
                    #summary = self.env['investment.land.overheads'].search([('id','=',transaction.id),('header_id','=',line.id)])
                    if overhead.code.id == transaction.id:

                        code = transaction.id
                        description = transaction.description
                        fee_charged += overhead.fee_charged
                        vat += overhead.vat
                        total_cost += overhead.total_cost
            if total_cost>0:
                self.env['sale.investment.overheads.summary'].create({'header_id':self.id,'code':code,'fee_charged':fee_charged,'vat':vat,
                    'total_cost':total_cost,'description':description})


        #now mark as ready
        if self.percentage_allocation == 100:
            self.state = 'ready'
        else:
            raise ValidationError("Allocation should be 100%. Check allocation lines!")

    @api.one
    def reset_to_draft(self):
        self.state = 'draft'

    @api.one
    def create_draft_invoices(self):
        setup = self.env['sale.investment.general.setup'].search([('id','=',1)])
        if self.state == 'ready' and self.posted == True:
            for line in self.overhead_summary_ids:
                invoice = self.env['account.invoice'].create({'partner_id':setup.provisional_vendor.id,'state':'draft','account_id':setup.provisional_vendor.property_account_payable.id,'name':'Draft Overheads Invoice',
                    'type':'in_invoice'})
                self.env['account.invoice.line'].create({'invoice_id':invoice.id,'account_id':setup.provisions_for_overheads.id,'name':'Project Overheads::'+line.description,'quantity':1,'price_unit':line.total_cost})


class project_costing_lines(models.Model):
    _name = 'investment.project.costing.lines'

    header_id = fields.Many2one('investment.project.costing.header','Lines',ondelete='cascade', select=True)

    unit_of_measure = fields.Selection([('acre',"Acre"),('hectare',"Hectare")])
    size_of_plots = fields.Float()
    allocation_percentage = fields.Float()
    acreage_to_use = fields.Float()
    no_of_plots = fields.Integer()
    #acreage_used = fields.Float()
    acreage_balance = fields.Float()
    land_purchase_cost = fields.Float()
    land_cost_per_plot = fields.Float(compute = 'compute_line_totals')
    overheads = fields.Float(compute = 'compute_overheads')
    total_cost = fields.Float(compute = 'compute_line_totals')
    margin = fields.Float(compute = 'compute_line_totals')
    price = fields.Float(compute = 'compute_line_totals')
    price_per_plot = fields.Float(compute = 'compute_line_totals')
    line_ids = fields.One2many('investment.land.overheads','header_id', 'Overheads', copy = True)


    @api.one
    @api.onchange('size_of_plots','acreage_to_use')
    def compute_no_of_plots(self):
        if (self.size_of_plots > 0) and (self.acreage_to_use>0):
            #no_of_plots = (self.allocation_percentage * self.header_id.useful_acreage * 0.01)/self.size_of_plots
            no_of_plots = self.acreage_to_use / self.size_of_plots
            #land_cost = self.allocation_percentage * 0.01 * self.header_id.purchase_cost
            land_cost = ((self.acreage_to_use -(self.acreage_to_use % self.size_of_plots)) / self.header_id.useful_acreage) * self.header_id.purchase_cost
            self.no_of_plots = no_of_plots
            self.land_purchase_cost = land_cost
            self.land_cost_per_plot = land_cost / no_of_plots
            #self.acreage_used = self.size_of_plots * self.no_of_plots
            self.acreage_balance = self.acreage_to_use % self.size_of_plots

    @api.one
    @api.depends('line_ids')
    def compute_overheads(self):
        total = 0.0
        for line in self.line_ids:
            total += line.total_cost
        self.overheads = total

    @api.one
    @api.depends('overheads','land_purchase_cost','header_id')
    def compute_line_totals(self):
        land_cost = 0.0
        margin = 0.0

        land_cost = self.land_purchase_cost + self.overheads
        margin = (self.land_purchase_cost + self.overheads) * self.header_id.profit_margin * 0.01
        price = land_cost + margin
        if self.no_of_plots > 0:#avoid dividebyzero exception
            price_per_plot = price / self.no_of_plots
            self.land_cost_per_plot = land_cost / self.no_of_plots
        else:
            price_per_plot = 0.0

        self.total_cost = land_cost
        self.margin = margin
        self.price = price
        self.price_per_plot = price_per_plot


class land_overheads(models.Model):
    _name = 'investment.land.overheads'
    _rec_name = 'description'

    header_id = fields.Many2one('investment.project.costing.lines',ondelete = 'cascade', select = True)
    code = fields.Many2one('investment.land.transactions')
    description = fields.Char()
    fee_charged = fields.Float()
    vat = fields.Float()
    total_cost = fields.Float()
    profit_margin = fields.Float()
    overhead_price = fields.Float(string = "Total Cost + Profit Margin")


    @api.onchange('code')
    def get_overhead_cost(self):
        transaction = self.env['investment.land.transactions'].search([('id','=',self.code.id)])
        self.description = transaction.description

        overhead = self.env['investment.land.transaction.costs'].search([('overhead.id','=',transaction.id)])
        if overhead.based_on == 'flat':
            self.fee_charged = overhead.cost
            if transaction.attracts_vat:
                self.vat = 0.16 * self.fee_charged
                self.total_cost = 1.16 * self.fee_charged
            else:
                self.total_cost = self.fee_charged
        elif overhead.based_on == 'percentage':
            self.fee_charged = (overhead.percentage*0.01) * self.header_id.land_purchase_cost
            if transaction.attracts_vat:
                self.vat = 0.16 * self.fee_charged
                self.total_cost = 1.16 * self.fee_charged
            else:
                self.total_cost = self.fee_charged

class overheads_summary(models.Model):
    _name = 'sale.investment.overheads.summary'

    header_id = fields.Many2one('investment.project.costing.header')
    code = fields.Char()
    description = fields.Char()
    fee_charged = fields.Float()
    vat = fields.Float()
    total_cost = fields.Float()


class monthly_penalties(models.Model):
    _name = 'sale.investment.monthly.penalty'
    name = fields.Char()
    date = fields.Date()
    amount = fields.Float()
    created = fields.Boolean(default = False)
    posted = fields.Boolean(default = False)
    line_ids = fields.One2many('sale.investment.monthly.penalty.lines','no')


class monthly_penalty_lines(models.Model):
    _name = 'sale.investment.monthly.penalty.lines'
    no = fields.Char()
    investor_no = fields.Char()
    investor_name = fields.Char()
    invoice_no = fields.Char()
    invoice_amount = fields.Float()
    monthly_amount = fields.Float()


class plot_transactions(models.Model):
    _name = 'investment.land.transactions'

    name = fields.Char(string = 'Code')
    description = fields.Char()
    attracts_vat = fields.Boolean()
    #attracts_margin = fields.Boolean()

class land_overheads_setup(models.Model):
    _name = 'investment.land.transaction.costs'

    overhead = fields.Many2one('investment.land.transactions')
    description = fields.Char()
    based_on = fields.Selection([('flat',"Flat Rate"),('percentage',"Percentage")], default = 'flat')
    percentage = fields.Float()
    cost = fields.Float()

    @api.onchange('overhead')
    def get_transaction_name(self):
        self.description = self.env['investment.land.transactions'].search([('id','=',self.overhead.id)]).description


class land_overheads_setup_local(models.Model):
    _name = 'investment.land.transaction.costs.local'
    _inherit = 'investment.land.transaction.costs'

    project_id = fields.Many2one('investment.project.costing.header')

class general_setup(models.Model):
    _name = 'sale.investment.general.setup'

    name = fields.Char()
    investor_application_nos = fields.Many2one('ir.sequence')
    investor_nos = fields.Many2one('ir.sequence')
    investor_closure_nos = fields.Many2one('ir.sequence')
    investor_activation_nos = fields.Many2one('ir.sequence')
    project_nos = fields.Many2one('ir.sequence')
    land_asset_account = fields.Many2one('account.account')#stock input and stock output account
    land_income_account = fields.Many2one('account.account')#product sales
    land_expense_account = fields.Many2one('account.account')#cost of goods sold
    inbound_from_location = fields.Many2one('stock.location')
    inbound_to_location = fields.Many2one('stock.location')
    outbound_from_location = fields.Many2one('stock.location')
    outbound_to_location = fields.Many2one('stock.location')
    land_input_account = fields.Many2one('account.account')
    land_output_account = fields.Many2one('account.account')
    provisions_for_overheads = fields.Many2one('account.account')
    provisional_vendor = fields.Many2one('res.partner', domain = [('supplier','=',True)])
    reservation = fields.Boolean(string = "Automatically Cancel Overdue Reservations", help = "Automatically cancel overdue reservations")
    reservation_period = fields.Integer(string = "Reservation Period(days)")

    @api.one
    def product_init(self):
        products = self.env['product.template'].search([('product_category','=','land')])
        for product in products:
            #product.check_purchasable()
            self.env['stock.inventory.line'].create({'inventory_id':13,'location_id':12,'product_id':product.id,'product_qty':1,'theoretical_qty':0})

    @api.one
    def investor_init(self):
        investors = self.env['res.partner'].search([('customer','=',True),('investor_no','!=',None)])
        investors.write({'investor':True})

class test(models.Model):
    _name = 'test'

    field1 = fields.Char()
    field2 = fields.Char()
    field3 = fields.Char()
    field4 = fields.Char()
    field5 = fields.Char()
    field6 = fields.Char()

class sale_investment_events(models.Model):
    _name = 'sale.investment.events'

    name = fields.Char(required = True)
    date = fields.Date(required = True)
    event_description = fields.Text()
    attendees = fields.One2many('sale.investment.event.attendees','event_id')

class sale_investment_event_attendees(models.Model):
    _name = 'sale.investment.event.attendees'

    event_id = fields.Many2one('sale.investment.event.attendees')
    name = fields.Char()
    email = fields.Char()
    mobile = fields.Char()
    organization = fields.Char()


class sale_investment_clan(models.Model):
    _name = 'sale.investment.clan'

    name = fields.Char(required = True)

class sale_investment_county(models.Model):
    _name = 'sale.investment.county'

    name = fields.Char(required = True)
