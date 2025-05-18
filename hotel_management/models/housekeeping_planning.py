from odoo import models, fields, api


class HousekeepingPlanning(models.Model):
    _name = 'housekeeping.planning'
    _description = 'Housekeeping Planning'

    staff_ids = fields.Many2one('staff.attendence',string='Housekeeping Staff')
    room_ids = fields.Many2many('hotel.rooms', string='Rooms')
    maintainance_type_ids = fields.Many2many('housekeeping.maintainance.type', string='Maintainance Type')