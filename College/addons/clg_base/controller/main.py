# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Student(http.Controller):
    
    @http.route(['/college'],website=True,auth='public')
    def college(self,**post):
        return request.render('clg_base.tmpl_college',{})
    
    @http.route('/college/student',website=True,auth='public')
    def student_details(self,**post):
        students = request.env['clg.student'].sudo().search([])
        return request.render('clg_base.tmpl_student_details',{'stud_details':students})
    
    @http.route('/college/staff/add',type="http",website=True,auth='public',csrf=False)
    def create_staff(self,**post):
        department_ids = request.env['clg.department'].sudo().search([])
        if request.httprequest.method == 'POST':
            request.env['clg.staff'].create(post)
            return request.render("clg_base.staff_add_success", {})
        return request.render('clg_base.staff_create_form',{'department':department_ids})
