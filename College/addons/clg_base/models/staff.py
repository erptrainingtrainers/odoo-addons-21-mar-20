
from odoo import api, fields, models, _

class Staff(models.Model):
    _name = 'clg.staff'
    _description = "Staff"
    _inherits = {"res.partner":'partner_id'}
    
#     name = fields.Char(string="First Name",required=True,tracking=True,index=True)
    last_name = fields.Char(string="Last Name",tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    dob = fields.Date(string="Date of Birth",tracking=True)
    department_id = fields.Many2one('clg.department',string="Department",ondelete="set null",tracking=True)
    language_ids = fields.Many2many('clg.language',string="Languages known")
    partner_id = fields.Many2one('res.partner',string="Contact")
    student_id = fields.Many2one('clg.student',string="Student")