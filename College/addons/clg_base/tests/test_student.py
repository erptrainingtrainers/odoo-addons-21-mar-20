# -*- coding: utf-8 -*-
from odoo.tests import common,new_test_user

class TestStudentCommon(common.TransactionCase):
    
    def setUp(self):
        super(TestStudentCommon, self).setUp()

        self.department = self.env['clg.department'].create({'name':'BBA'})
        self.department2 = self.env['clg.department'].create({'name':'B.Ed'})
        self.student = self.env['clg.student'].create({'name': 'Test','last_name':'Augustin','roll_no':'34534437347','department_id':self.department.id})
        
    def test_check_student_department(self):
        self.assertEqual(self.department.id, self.student.department_id.id)
        
    def test_user_level(self):
        self.user = new_test_user(self.env, login='test1', groups='clg_base.group_clg_user',department_id=self.department2.id)
        self.student.with_user(self.user).write({'description':"New Description"})