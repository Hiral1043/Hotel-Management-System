from odoo import models, fields, api

class HotelFoodItem(models.Model):
    _name = 'hotel.food.item'
    _description = 'Hotel Food Item'

    name = fields.Char(string='Food Item Name', required=True)
    description = fields.Text(string='Description')
    food_image =  fields.Image()
    price = fields.Float(string='Price', required=True)
    restaurant_id = fields.Many2one('hotel.restaurant', string='Restaurant',ondelete='cascade')


    def order_meal(self):
        booking_id = self.env.context.get('booking_id')

        booking = self.env['hotel.booking.lines'].browse(booking_id)

        booked_id = booking.booking_id

        # print("\n\n\n\n\n>>>>>>>>.booked_id",booked_id)
        if booking:
            # print("\n\n\n\n\n\n>>>>>>>>>>>>booking",booking)
            self.env['restaurant.order.lines'].create({
                'reservation_id': booked_id.id,
                'food_item_id': self.id,
                'price': self.price,
                'quantity': 1,
            })
        # })
            # print("\n\n\n\n>>>>>>>>>>",booking)
        # return {
        #     'name': 'Room Reservation',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hotel.room.reservation',
        #     'res_id': booking.id,
        #     'view_mode': 'form',
        #     'target': 'current'
        # }