from odoo import models, fields, api
from odoo.exceptions import UserError

class Student_Remark(models.TransientModel):
    _name = 'wizard.student.remark'
    _description = 'Student Remark'
    
    remark = fields.Text(string="Remark")
    student_id = fields.Many2one('clg.student',string="Student")
    
    def action_confirm(self):
        self.student_id.write({'remarks':str(self.student_id.remarks)+self.remark})