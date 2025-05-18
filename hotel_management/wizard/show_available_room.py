from odoo import api,models,fields
from odoo.exceptions import UserError
class ShowAvailableRoom(models.TransientModel):
    _name = "available.room.wizard"
    _description = "Available Room Wizard"

    check_in_date = fields.Date(string="Check-in Date", required=True)
    check_out_date = fields.Date(string="Check-out Date", required=True)
    adults = fields.Integer(string = "Number of Adults", default=1, required=True)
    child = fields.Integer(string = "Number of child")
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", required=True)
    room_reservation_id = fields.Many2one('hotel.room.reservation', string="Room Reservation")

    def action_search(self):
        for record in self:
            if record.adults <= 0 and record.child <= 0:
                raise UserError("please enter Adults or child")

            if record.check_in_date <= record.check_out_date and record.check_in_date >= fields.Date.today():
                reservation = self.env['hotel.room.reservation'].search([
                    ('check_in_date', '<=', record.check_out_date),
                    ('check_out_date', '>=', record.check_in_date),
                    ('room_id.hotel_id', '=' ,self.hotel_id.id),
                ])
                booked_rooms = reservation.mapped('room_id.id')
                available_room = self.env['hotel.rooms'].search([
                    ('id', 'not in', booked_rooms),
                    ('room_status', '=', 'available'),
                    ('capacity', '>=', self.adults + self.child),
                    
                ])
                if available_room.ids == []:
                    raise UserError("No available rooms found based on your preferences.")
                
                print("\n\n\n\n\n\n\n\n\n>>>available_room ",available_room)
                available_rooms_filter = available_room
            
            else:
                raise UserError("Please enter proper check-in & check-out Dates ")
        kanban_view_id = self.env.ref('hotel_management.hotel_room_available_view_kanban').id
        form_view_id = self.env.ref('hotel_management.view_hotel_rooms_available_form').id
    
        return {
            'name': 'Available Rooms',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.rooms',
            'view_mode': 'kanban,form', 
            'views': [(kanban_view_id, 'kanban'), (form_view_id, 'form')], 
            'domain': [('id', 'in', available_rooms_filter.ids),('hotel_id', '=', self.hotel_id.id)],  
            'target': 'current',
            'context': {
                'check_in_date': self.check_in_date,
                'check_out_date': self.check_out_date,
                'adults': self.adults,
                'child': self.child,
                'hotel_id': self.hotel_id.id,
                'room_reservation_id': self.room_reservation_id.id} 
            
        }

    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window_close',
        }