from openerp import models, fields, api

class investor_next_of_kin(models.Model):
    _inherit = 'next.of.kin'

    investor_id = fields.Many2one('res.partner')
    investor_app_id = fields.Many2one('sale.investor.registration')

class investor(models.Model):
    _inherit = 'res.partner'


    investor = fields.Boolean()
    investor_no = fields.Char()
    next_of_kin_ids = fields.One2many('next.of.kin','investor_id')
    dob = fields.Date(string = 'Date of Birth')
    idno = fields.Char(string = 'ID No.')
    passport_no = fields.Char(string = 'Passport No.')
    investor_pin = fields.Char(string = 'Investor PIN')
    marital_status = fields.Selection([('single',"Single"),('married',"Married")])
    gender = fields.Selection([('male',"Male"),('female',"Female")])
    occupation = fields.Char()
    is_kcit = fields.Boolean(string='KCIT Member')

class investor_category(models.Model):
    '''
    This extension is to allow us to associate investors with projects.
    The associated projects will be listed under customer tags allowing us to search for customers
    per project. We'll also add a report on the same
    '''
    _inherit = 'res.partner.category'

    project_id = fields.Many2one('product.category')
