from odoo import models, fields, api

class HousekeepingMaintainanceService(models.Model):
    _name = 'maintainance.service'
    _description = "Housekeeping Maintainance Service"

    maintainance_date = fields.Date(string="Maintainance Date")
    
    maintainance_type_id = fields.Many2one('housekeeping.maintainance.type', string="Maintainance Type")

    status = fields.Selection([('pending', 'Pending'),
                                ('completed', 'Completed')], 
                                string="Status", default='pending')
    room_id = fields.Many2many('hotel.rooms', string="Room")
    services = fields.Many2many('housekeeping.check.list', string="Services")
    staff_ids = fields.One2many('staff.attendence','maintainance_service_id', string="Staff")

