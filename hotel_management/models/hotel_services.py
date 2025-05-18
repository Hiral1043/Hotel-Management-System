from odoo import models,fields,api

class HotelRoomService(models.Model):
    _name = 'hotel.room.service'
    _description = 'Hotel Room Service'

    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", required=True)
    service_type = fields.Selection(
        [
            ('room_service', 'Room Service'),
            ('spa', 'Spa'),
            ('restaurant', 'Restaurant'),
            ('laundry', 'Laundry'),
            ('fitness', 'Fitness Center'),
            ('housekeeping', 'Housekeeping'),
        ],
        string='Service Type',
        required=True,
        help="Select the type of service"
    )

    service_name = fields.Char(string="Service Name", required=True)
    price = fields.Float(string="Price")