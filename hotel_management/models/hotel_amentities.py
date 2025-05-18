from odoo import models,fields,api


class HotelAmenities(models.Model):
    _name = 'hotel.amenities'
    _description = 'Hotel Amenities'

    hotel_id = fields.Many2one("hotel.hotel")
    amenity_type = fields.Selection(
        [   ('room_amenities','Room Amenities'),
            ('garden', 'Garden'),
            ('swimming_pool', 'Swimming Pool'),
            ('spa', 'Spa'),
            ('gym', 'Gym'),
            ('restaurant', 'Restaurant')
        ],
        string='Amenity Type',
        required=True,
    )
    name = fields.Char(string='Amenity Name', required=True)
    description = fields.Text(string='Description')
    reservation_amenitites_id = fields.Many2one('hotel.room.reservation', string="Reservation ID")
