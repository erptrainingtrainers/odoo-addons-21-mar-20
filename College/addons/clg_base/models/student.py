from odoo import api, fields, models, _

class Student(models.Model):
    _name = "clg.student"
    _inherit = 'image.mixin'
    _description = "Student"
    
    name = fields.Char(string="First Name",required=True)
    last_name = fields.Char(string="Last Name")
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age")
    admitted_date = fields.Datetime(string="Admitted Date and time")
    tc_12 = fields.Binary(string="12th TC")
    remarks = fields.Text(string="Remarks")
    description = fields.Html(string="Description")
    
class Department(models.Model):
    _name = "clg.department"
    _description = "Department"
    
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    abbreviation = fields.Char(string="Abbreviation")
    
    
    