from odoo import models,fields,api

class HotelRoomType(models.Model):
    _name = "hotel.room.type"

    name = fields.Char(string='Room Type Name', required=True)
    capacity = fields.Integer(string='Capacity', required=True)
    price_per_night = fields.Float(string='Price per Night', required=True)
    is_ac = fields.Selection([
        ('yes', 'AC'),
        ('no', 'NON-AC')
    ], string="Air Conditioning", required=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Room type name must be unique!')
    ]