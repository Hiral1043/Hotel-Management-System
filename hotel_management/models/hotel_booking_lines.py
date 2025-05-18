from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class HotelBookingLines(models.Model):
    _name = 'hotel.booking.lines'
    _description = 'Hotel Booking Lines'

    room_id = fields.Many2one('hotel.rooms', string="Room")
    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')], string="Discount Type")
    discount = fields.Float(string="Discount")
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)
    price_type = fields.Selection([
        ('season', 'Season'),
        ('discount', 'Discount')], string="Price Type")
    price_list_id = fields.Many2one('hotel.pricelist', string="Price List")
    room_type_id = fields.Many2one('hotel.room.type')
    check_in_date = fields.Date(string="Check In Date")
    check_out_date = fields.Date(string="Check Out Date")
    total_days = fields.Float(string="Total Days", compute="_compute_total_days", store=True)
    booking_id = fields.Many2one('hotel.room.reservation', string="Booking Reference", required=True, ondelete='cascade')

    @api.depends('check_in_date', 'check_out_date')
    def _compute_total_days(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                record.total_days = (record.check_out_date - record.check_in_date).days
            else:
                record.total_days = 0

    def add_meal(self):
        kanban_view_id = self.env.ref('hotel_management.hotel_food_item_view_kanban').id
        
        return {
            'name': 'Food items',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.food.item',
            'view_mode': 'kanban',
            'views': [(kanban_view_id, 'kanban')],
            # 'domain': [('id', 'in', available_rooms_filter.ids), ('hotel_id', '=', self.hotel_id.id)],  # Show rooms in the selected hotel
            'target': 'current',
            'context': {'booking_id': self.id}
        }
    
    @api.depends('room_id', 'booking_id.check_in_date', 'booking_id.check_out_date', 'booking_id.price_list_id', 'room_type_id', 'discount', 'discount_type')
    def _compute_amount(self):
        for line in self:
            if not line.room_id or not line.booking_id:
                continue

            room = line.room_id
            booking = line.booking_id

            pricelist_item = self.env['room.pricelist.item'].search([
                ('pricelist_id', '=', booking.price_list_id.id),
                ('room_type_id', '=', room.room_type_id.id),
                ('start_date', '<=', booking.check_in_date),
                ('end_date', '>=', booking.check_out_date),
            ], limit=1)

            if pricelist_item:
                line.price_type = pricelist_item.price_type
                line.amount = pricelist_item.final_price
                # print("\n\n\n\n\n\n>>>>>>>>>>>amount",line.amount)
                if pricelist_item.discount_type == 'fixed':
                    line.discount = pricelist_item.discount_fixed
                    # print("\n\n\n\n\n\n>>>>>>>>>>>discount",line.discount)
                elif pricelist_item.discount_type == 'percentage':
                    line.discount = pricelist_item.discount_percentage
                else:
                    line.discount = 0.0
                line.discount_type = pricelist_item.discount_type
            else:
                line.price_type = False
                line.discount = 0.0
                line.discount_type = False
                line.amount = room.price
