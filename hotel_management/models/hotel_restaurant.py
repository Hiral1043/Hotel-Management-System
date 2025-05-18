from odoo import models, fields

class HotelRestaurant(models.Model):
    _name = 'hotel.restaurant'
    _description = 'Hotel Restaurant'

    name = fields.Char(string='Restaurant Name', required=True)
    restaurant_image = fields.Image()
    food_item_ids = fields.One2many('hotel.food.item', 'restaurant_id', string="Food Items")
    description = fields.Text()
    address = fields.Text()
    ratings = fields.Selection([('1', 'normal'), ('2', '2 star'), ('3', '3 star'), ('4', '4 star'), ('5', '5 star'), ('7', '7 star')], default='2')
    booking_id = fields.Many2one("hotel.room.reservation")