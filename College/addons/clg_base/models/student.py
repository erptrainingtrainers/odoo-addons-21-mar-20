from odoo import api, fields, models, _

class Student(models.Model):
    _name = "clg.student"
    _inherit = 'image.mixin'
    _description = "Student"
    
    name = fields.Char(string="First Name",required=True)
    last_name = fields.Char(string="Last Name")
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    dob = fields.Date(string="Date of Birth")
    height = fields.Float(string="height")
    age = fields.Integer(string="Age")
    admitted_date = fields.Datetime(string="Admitted Date and time")
    tc_12 = fields.Binary(string="12th TC")
    remarks = fields.Text(string="Remarks")
    description = fields.Html(string="Description")
    department_id = fields.Many2one('clg.department',string="Department",ondelete="set null")
    language_ids = fields.Many2many('clg.language',string="Languages known")
    education_ids = fields.One2many('stud.education','student_id',string="Education Details",help="Previous Education Details")
    attachment_ids = fields.Many2many('ir.attachment',string="Attachment")
    
class Department(models.Model):
    _name = "clg.department"
    _description = "Department"
    
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    abbreviation = fields.Char(string="Abbreviation")
    
class Languages(models.Model):
    _name = 'clg.language'
    _description = "Language"
    
    name = fields.Char(string="Name")
    
class Education(models.Model):
    _name = 'stud.education'
    _description = "Education"
    
    student_id = fields.Many2one('clg.student')
    level = fields.Char(string="Level")
    program = fields.Char(string="Progarm")
    mode = fields.Selection([('regular','Regular'),('private','Private'),('not_applicable','Not Applicable')],string="Mode")
    
    