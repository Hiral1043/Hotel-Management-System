from odoo import models,fields,api

class HotelRoomPrice(models.Model):
    _name = 'hotel.room.price'
    _description = 'Hotel Room Price'

    

    room_type_id = fields.Many2one('hotel.room.type', string="Room Type", required=True)
    season_id = fields.Many2one('hotel.season', string="Season", required=True)
    price = fields.Float(string="Price", required=True)
    discount_type = fields.Selection([('fixed', 'Fixed'), ('percentage', 'Percentage')], string="Discount Type")
    discount_value = fields.Float(string="Discount Value")