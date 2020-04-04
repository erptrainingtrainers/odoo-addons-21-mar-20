from odoo import models, fields, api
from odoo.exceptions import UserError

class Student_details_report(models.TransientModel):
    _name = 'wizard.student.report'
    _description = 'Student Report'
    
    state = fields.Selection([('draft','Draft'),('admitted','Admitted'),('completed','Completed'),('dis-continue','Dis-Continue')],string="State",tracking=True)
    
    def print_report(self):
        data = {
            'model':'wizard.student.report',
            'form':self.read()[0],
            'record_ids':self.env['clg.student'].search([('state','=',self.state)]).ids,
            }
        return self.env.ref('clg_base.clg_student_details_report').report_action(self,data=data)
        
        
