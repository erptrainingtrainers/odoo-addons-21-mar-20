from odoo import api, fields, models, _
from datetime import datetime
from odoo.exceptions import UserError
from odoo.osv import expression
from lxml import etree
from odoo.addons.base.models.ir_mail_server import MailDeliveryException

class Student(models.Model):
    _name = "clg.student"
    _inherit = ['image.mixin','mail.thread','mail.activity.mixin','clg.member']
    _description = "Student"
    _order = "last_name,roll_no"
    _sql_constraints = [
        ('student_roll_no_uniq', 'unique (roll_no)', "Roll No. is Unique for a Student"),
    ]
    
    @api.model
    def default_get(self, fields_list):
        result = super(Student, self).default_get(fields_list)
        result['remarks'] = "Good"
        result['user_id'] = self.env.user.id
        return result
    
    @api.model
    def fields_get(self,fields=None,attributes=None):
        result = super(Student,self).fields_get(fields,attributes)
        return result
    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', context=None, toolbar=False,submenu=False):    
        result = super(Student, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        if view_type in ['form','tree']:
            doc = etree.XML(result['arch'])
            if self._context.get('label',False):
                for node in doc.xpath("//field[@name='roll_no']"):
                    node.set('string', self._context.get('label'))
            result['arch'] = etree.tostring(doc)
        return result
    
    name = fields.Char(string="First Name",required=True,tracking=True,index=True,size=15)
    last_name = fields.Char(string="Last Name",tracking=True)
    roll_no = fields.Char(string="Roll No.",required=True)
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender",default='male')
    dob = fields.Date(string="Date of Birth",tracking=True)
    height = fields.Float(string="height")
    age = fields.Integer(string="Age",group_operator=False)
    admitted_date = fields.Datetime(string="Admitted Date and time",tracking=True,default=fields.Datetime.now())
    tc_12 = fields.Binary(string="12th TC")
    remarks = fields.Text(string="Remarks",tracking=True,readonly=False,groups="clg_base.group_clg_manager")
    description = fields.Html(string="Description")
    department_id = fields.Many2one('clg.department',string="Department",ondelete="set null",tracking=True)
    language_ids = fields.Many2many('clg.language',string="Languages known",domain=[])
    education_ids = fields.One2many('stud.education','student_id',string="Education Details",help="Previous Education Details")
    attachment_ids = fields.Many2many('ir.attachment',string="Attachment")
    edu_id = fields.Many2one('stud.education',string='Education')
    country_id = fields.Many2one('res.country',string="Country")
    lang_known_count = fields.Integer(compute="_compute_lang_known_count",inverse="_inverse_change_remarks",string='Lang known count',store=False)
    state = fields.Selection([('draft','Draft'),('admitted','Admitted'),('completed','Completed'),('dis-continue','Dis-Continue')],string="State",tracking=True)
    user_id = fields.Many2one('res.users',string="User")
    tenth_mark = fields.Integer(string="10th Mark")
    admission_no = fields.Char(string="Admission No")
    
    def name_get(self):
        result = []
        for record in self:
            if record.name and record.roll_no:
                result.append((record.id, record.name + ' %s [%s]' % (record.last_name or '',record.roll_no)))
            if record.name and not record.roll_no:
                result.append((record.id, record.name))
        return result
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('roll_no', operator, name)]
        rec = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return models.lazy_name_get(self.browse(rec).with_user(name_get_uid))
    
    @api.returns('self', lambda value: value.id)
    def copy(self,default=None):
        raise UserError(_('You cannot duplicate student.'))
    
    @api.onchange('dob')
    def _onchange_get_age(self):
        if self.dob:
            self.age = datetime.now().year - self.dob.year
            
    @api.constrains('dob')
    def _validate_dob(self):
        if self.dob:
            if self.dob > datetime.now().date():
                raise UserError("Sorry! The Date of birth cannot be futuristic.")
            
    @api.depends('language_ids')
    def _compute_lang_known_count(self):
        self.lang_known_count = False
        if self.language_ids:
            self.lang_known_count = len(self.language_ids)
    
    def _inverse_change_remarks(self):
        if self.remarks:
            self.remarks = self.remarks.upper()
    
    def draft_to_admit(self):
        self.state = 'admitted'
        
    def admit_to_completed(self):
        self.state = 'completed'
        return {
            'effect':{
                'fadeout':'slow',
                'message':'You have completed your Degree',
                'type': 'rainbow_man'
                }
            }
        
    def admit_to_dis_continue(self):
        self.state = 'dis-continue'
    
    def action_send_email(self):
        template_id = self.env.ref('clg_base.email_template_clg_student')
        try:
            template_id.send_mail(self.id,force_send=True)
        except MailDeliveryException:
            print("MailDeliveryException")
        except Exception:
            print("Exception")
    
    def action_move_to_admit(self):
        print(self._context.get('active_ids',False))
        record_ids = self._context.get('active_ids',False)
        records = self.search([('id','in',record_ids),('state','=','draft')])
        print(records)
        for rec in records:
            rec.write({'state':'admitted'})
        title = _("Student Admission!")
        message = _("Only draft records moved to admitted!")
        self.env['bus.bus'].sendone(
            (self._cr.dbname, 'res.partner', self.env.user.partner_id.id),
            {'type': 'simple_notification', 'title': title, 'message': message, 'sticky': True, 'warning': True})
        
    
    def get_details(self):
        print(self.search([]))
        print(self.search([],order="roll_no asc",limit=4))
        print("Mapped function")
        print(self.search([]).mapped('name'))
        print("Sorted")
        print(self.search([]).sorted(lambda id:id.name,reverse=True).mapped('name'))
        print("Filtered")
        print(self.search([]).filtered(lambda id:id.gender == 'male'))
        
    def open_new_url(self):
        return {
            "type": "ir.actions.act_url",
            "url": "https://google.com",
            "target": "new",
        }
        
    @api.model
    def create(self,vals):
#         vals['state'] = 'admitted'
        sequence_code = 'student.admission.number'
        vals['admission_no'] = self.env['ir.sequence'].next_by_code(sequence_code)
        student = super(Student,self).create(vals)
        student.state = 'draft'
        return student
    
    def write(self,vals):
        name = vals.get('name',False) or self.name
        last_name = vals.get('last_name',False) or self.last_name
#         if vals.get('state',False):
#             if not vals.get('state') == 'admitted':
#                 raise UserError(_("Sorry! You can complete this from Admitted state only."))
        
        if name:
            vals['name'] = name.upper()
        if last_name:
            vals['last_name'] = last_name.upper()
#         if vals.get('last_name',False):
#             if vals.get('last_name',False) != self.last_name:
#                 raise UserError(_("Sorry! You cannot update the last name."))
        student = super(Student,self).write(vals)
        return student
    
    def unlink(self):
        if self.state in ['admitted','completed','dis-continue']:
            raise UserError(_("Sorry! You cannot delete the Admitted/Completed/Dis-continued Students."))
        result = super(Student, self).unlink()
        return result
    
class Department(models.Model):
    _name = "clg.department"
    _description = "Department"
    
    name = fields.Char(string="Name")
    code = fields.Char(string="Code",copy=False)
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
    
    name = fields.Char(string="Name",required=True)
    color = fields.Integer('Color Index')
    
class Education(models.Model):
    _name = 'stud.education'
    _description = "Education"
    _rec_name = "program"
    
    student_id = fields.Many2one('clg.student')
    level = fields.Char(string="Level")
    program = fields.Char(string="Progarm")
    mode = fields.Selection([('regular','Regular'),('private','Private'),('not_applicable','Not Applicable')],string="Mode")
    
    