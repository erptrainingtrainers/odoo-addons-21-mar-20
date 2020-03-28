from odoo import api, fields, models, _

class Member(models.AbstractModel):
    _name = 'clg.member'
    _description = "Member"
    
    email = fields.Char(string='Email')
    mobile = fields.Char(string='Mobile')