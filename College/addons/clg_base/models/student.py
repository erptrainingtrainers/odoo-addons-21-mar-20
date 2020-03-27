from odoo import api, fields, models, _

class Student(models.Model):
    _name = "clg.student"
    _inherit = ['image.mixin','mail.thread','mail.activity.mixin']
    _description = "Student"
    
    name = fields.Char(string="First Name",required=True,tracking=True)
    last_name = fields.Char(string="Last Name",tracking=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    dob = fields.Date(string="Date of Birth",tracking=True)
    height = fields.Float(string="height")
    age = fields.Integer(string="Age")
    admitted_date = fields.Datetime(string="Admitted Date and time",tracking=True)
    tc_12 = fields.Binary(string="12th TC")
    remarks = fields.Text(string="Remarks",tracking=True)
    description = fields.Html(string="Description")
    department_id = fields.Many2one('clg.department',string="Department",ondelete="set null",tracking=True)
    language_ids = fields.Many2many('clg.language',string="Languages known")
    education_ids = fields.One2many('stud.education','student_id',string="Education Details",help="Previous Education Details")
    attachment_ids = fields.Many2many('ir.attachment',string="Attachment")
    edu_id = fields.Many2one('stud.education',string='Education')
    country_id = fields.Many2one('res.country',string="Country")
    
class Department(models.Model):
    _name = "clg.department"
    _description = "Department"
    
    name = fields.Char(string="Name")
    code = fields.Char(string="Code")
    abbreviation = fields.Char(string="Abbreviation")
    students_count = fields.Integer(compute="_compute_student_count",string="Stud. Count")
    
    def _compute_student_count(self):
        for record in self:
            record.students_count = self.env['clg.student'].search_count([('department_id','=',record.id)])
    
    def open_dept_students(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Students'),
            'res_model': 'clg.student',
            'view_mode': 'tree,form',
            'domain':[('department_id','=',self.id)],
            'context': {'default_department_id': self.id},
            }
    
class Languages(models.Model):
    _name = 'clg.language'
    _description = "Language"
    
    name = fields.Char(string="Name")
    
class Education(models.Model):
    _name = 'stud.education'
    _description = "Education"
    _rec_name = "program"
    
    student_id = fields.Many2one('clg.student')
    level = fields.Char(string="Level")
    program = fields.Char(string="Progarm")
    mode = fields.Selection([('regular','Regular'),('private','Private'),('not_applicable','Not Applicable')],string="Mode")
    
    