from odoo import models, fields, api
from odoo.exceptions import UserError

class StudentSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    max_fee_limit = fields.Float(string="Max. Fee Limit",config_parameter='clg_base.max_fee_limit')
