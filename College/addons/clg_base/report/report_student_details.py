from odoo import models, fields, api
from odoo.exceptions import UserError

class Student_details_report(models.AbstractModel):
    _name = 'report.clg_base.report_student_details'
    
    def get_completed_records(self):
        count = self.env['clg.student'].search_count([('state','=','completed')])
        return count
    
    @api.model
    def _get_report_values(self, docids, data=None):
        if data.get('category',False):
            docs = self.env['clg.student'].browse(data['record_ids'])
            return {
                'docs': docs,
                'form':data['form'],
                'get_completed_records':self.get_completed_records(),
            }
        else:
            docs = self.env['clg.student'].browse(docids)
            return {
                'doc_ids': self.ids,
                'docs': docs,
                'get_completed_records':self.get_completed_records(),
            }
