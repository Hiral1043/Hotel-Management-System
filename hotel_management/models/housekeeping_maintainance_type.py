from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HousekeepingMaintainanceType(models.Model):
    _name = 'housekeeping.maintainance.type'
    _description = 'Housekeeping Maintainance Type'

    name = fields.Char(string='Maintainance Type', required=True)
    staff_ids = fields.Many2many('staff.attendence', string='Housekeeping Staff')
    maintainance_service_ids = fields.One2many('maintainance.service', 'maintainance_type_id', string='Maintainance Services')
    check_list = fields.Many2many('housekeeping.check.list', string='Check List')



    