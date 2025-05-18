from odoo import models, fields, api
from odoo.exceptions import UserError

class HousekeepingStaffAttendence(models.Model):
    _name = 'staff.attendence'
    _description = 'Housekeeping Staff Attendence'

    staff_id = fields.Many2one('hotel.housekeeping.staff', string='Staff', required=True)
    check_in_time = fields.Datetime(string='Check In Time', required=True)
    check_out_time = fields.Datetime(string='Check Out Time')
    maintainance_service_id = fields.Many2one('maintainance.service', string='Maintainance Service')

    