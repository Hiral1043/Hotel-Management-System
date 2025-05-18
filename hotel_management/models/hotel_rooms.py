from odoo import models,fields,api,_
from odoo.exceptions import ValidationError,UserError

class HotelRooms(models.Model):
    _name = "hotel.rooms"
    _description = 'Hotel Rooms'
    _rec_name = 'room_no'

    room = fields.Char(string="room",required=True, copy=False, readonly=False,
        default= lambda self: _('New'))
    
    hotel_id = fields.Many2one('hotel.hotel')
    room_no = fields.Integer(string="Room Number")
    floor=fields.Integer(string="Floor")
    capacity = fields.Integer(string = "Capacity")
    price = fields.Float(string = "Base Price")
    price_id = fields.Many2one('hotel.room.price', string="Price")
    image = fields.Image(string="Room Image")
    room_status = fields.Selection([('available','Available'),
                                     ('maintenance','Maintenance')],default='available')
    room_type_id = fields.Many2one('hotel.room.type')
    reservation_id = fields.Many2one('hotel.room.reservation')
    discount = fields.Float(string="Discount Amount")
    show_add_button = fields.Boolean(compute="_compute_show_add_button", store=False)
    show_book_button = fields.Boolean(compute="_compute_show_add_button", store=False)
   
    @api.depends_context('active_model','active_id')
    def _compute_show_add_button(self):
        for rec in self:
            is_booking = rec.env.context.get('active_model') == 'hotel.room.reservation' and rec.env.context.get('active_id')
            rec.show_add_button = bool(is_booking)
            rec.show_book_button = not bool(is_booking)

    @api.model
    def create(self,vals): 
        if vals.get('room',_('New')) == _('New'):
            vals['room'] = self.env['ir.sequence'].next_by_code('hotel.rooms') or _('New')
            print("/n/n/n/n/n/n/n/n/n/n>>>>>>>>>>>>>>>>>>self",self)
            print("/n/n/n/n/n/n/n/n/n/n>>>>>>>>>>>>>>>>>>vals",vals)

        return super().create(vals)
    

    @api.onchange('room_type_id')
    def _onchange_room_type_id(self):
        self.price = self.room_type_id.price_per_night

    

    def book_room(self):

        return {
            'name': 'Book Rooms',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.room.reservation',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_check_in_date': self._context.get('check_in_date'),
                'default_check_out_date': self._context.get('check_out_date'),
                'default_adults': self._context.get('adults'),
                'default_child': self._context.get('child'),
                'default_room_id': self.id,
                'default_room_type_id': self.room_type_id.id,
                'default_room_no': self.room_no,
                'default_floor': self.floor,
                'default_hotel_id': self.hotel_id.id,
                'default_booking_lines_ids': [(0, 0, {
                    'room_id': self.id,
                    'room_type_id' : self.room_type_id.id,
                    # 'hotel_id' : self.hotel_id.id
                })]
            }
        }

    
    def add_extra_room(self):

        booking_id = self.env.context.get('booking_id')
        booking = self.env['hotel.room.reservation'].browse(booking_id)
        if booking:
            booking.write({ 
                'booking_lines_ids': [(0, 0, {
                    'room_id': self.id,
                })]
            })
            print("\n\n\n\n>>>>>>>>>>",booking)
        return {
            'name': 'Add Extra Room',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.room.reservation',
            'res_id': self._context.get('active_id'),
            'view_mode': 'form',
            'target': 'current'
            }         