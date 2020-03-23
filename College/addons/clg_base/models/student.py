from odoo import api, fields, models, _

class Student(models.Model):
    _name = "clg.student"
    _description = "Student"
    
    name = fields.Char(string="Name",required=True)