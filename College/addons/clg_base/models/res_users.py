from odoo import api, fields, models, _

class Users(models.Model):
    _inherit = 'res.users'
    
    department_id = fields.Many2one('clg.department',string="Department")