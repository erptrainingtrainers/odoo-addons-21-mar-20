from odoo import models, fields, api
from odoo.exceptions import UserError

class Student_details_report(models.AbstractModel):
    _name = 'report.clg_base.report_student_details'
    
    def get_completed_records(self):
        count = self.env['clg.student'].search_count([('state','=','completed')])
        print(count)
        return count
    
    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['clg.student'].browse(data['record_ids'])
#         if data:
#             docs = self.env['clg.student'].browse(data['record_ids'])
#         else:
#             docs = self.env['clg.student'].browse(self._context.get('active_id'))
        return {
            'doc_ids': self.ids,
            'doc_model': data['model'],
            'docs': docs,
            'form':data['form'],
            'get_completed_records':self.get_completed_records,
        }
    
