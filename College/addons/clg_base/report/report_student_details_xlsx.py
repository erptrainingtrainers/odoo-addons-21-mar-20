from odoo import models,fields

class StudentXlsx(models.AbstractModel):
    _name = 'report.clg_student.report_student_details_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, students):
        print(data)
        print(students)
        dt_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        for obj in students:
            report_name = obj.name
            # One sheet by partner
            sheet = workbook.add_worksheet(report_name[:31])
            bold = workbook.add_format({'bold': True})
            sheet.set_column('A:A',20)
            sheet.set_column('B:B',30)
            sheet.write(0, 0, 'First Name', bold)
            sheet.write(1, 0, 'Last Name', bold)
            sheet.write(2, 0, 'Roll No.', bold)
            sheet.write(3, 0, 'Date of Birth', bold)
            sheet.write(4, 0, 'Admission No.', bold)
            sheet.write(5, 0, 'Email', bold)
            sheet.write(6, 0, 'Gender', bold)
            sheet.write(7, 0, 'Department', bold)
            
            sheet.write(0, 1, obj.name)
            sheet.write(1, 1, obj.last_name)
            sheet.write(2, 1, obj.roll_no)
            sheet.write(3, 1, obj.dob,dt_format)
            sheet.write(4, 1, obj.admission_no or '')
            sheet.write(5, 1, obj.email)
            sheet.write(6, 1, dict(self.env['clg.student']._fields['gender'].selection).get(obj.gender))
            sheet.write(7, 1, obj.department_id.name)
