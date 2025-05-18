from datetime import datetime
from odoo import models,fields,api,_,Command
from odoo.exceptions import ValidationError,UserError

class HotelRoomReservation(models.Model):
    _name = 'hotel.room.reservation'
    _description = 'Hotel Room Reservation'
    _rec_name = 'room_id'

    room_id = fields.Many2one('hotel.rooms',required=True)
    room_type_id = fields.Many2one('hotel.room.type',store=True)
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", default=lambda self: self.env['hotel.hotel'].search([], limit=1))
    adults = fields.Integer(string="Number of Adults", required=True)
    child = fields.Integer(string="Number of Child", required=True)
    room_no = fields.Integer(string="Room Number")
    floor = fields.Integer(string="Floor")
    room_type = fields.Char(string="Room Type")
    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    stay = fields.Integer(string="stay(days)", compute="_compute_days", store=True)
    status = fields.Selection([('confirm','Confirmed'),
                               ('check_in','Check-in'),
                               ('check_out','Check-out'),
                                ('cancel','Cancel')])
    
    
    room_status = fields.Selection([('available','Available'),
                                        ('occupied','Occupied')],default='available')
    
    available_rooms_ids = fields.Many2many('hotel.rooms',compute='compute_available_rooms',store=True)
    guest_photo = fields.Image(string="guest Photo", related='guest_id.guest_photo' ,store=True)
    guest_id = fields.Many2one('hotel.guest',string="Guest",store=True, required=True)
    guest_phone = fields.Char(string="Mobile No.")
    guest_gender = fields.Selection([('male','Male'),
                                     ('female','Female')])
    guest_dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age",  store=True)
    identity_proof = fields.Selection([('aadhar','Aadhar'),
                                       ('pan','Pan'),
                                       ('voter','Voter'),
                                       ('passport','Passport')],
                                       string="Identity Proof" ,required=True)
    identity_proof_number = fields.Char(string="Identity Proof Number" ,required=True) 
    identity_proof_image = fields.Binary(string="Identity Proof Image",  related='guest_id.identity_proof_image')
    show_available_room = fields.One2many('available.room.wizard', 'room_reservation_id', string="Show Available Room")
    booking_lines_ids = fields.One2many('hotel.booking.lines','booking_id', string="Booking Lines")
    members_ids = fields.Many2many('hotel.guest','guest_member_ids', string="Member")
    policiess_ids = fields.One2many('hotel.policy','hotel_id', related='hotel_id.policies_ids', string="Hotel Policies")
    total_guests = fields.Integer(string="Total Guests", compute="_compute_total_guest", store=True)
    price_list_id = fields.Many2one('hotel.pricelist', string="Price List")
    invoice_id = fields.Many2one('account.move')
    order_line_ids = fields.One2many('restaurant.order.lines', 'reservation_id', string="Order Lines", ondelete='cascade')


    @api.onchange('room_type')
    def _onchange_room_id(self):
        self.room_type = self.room_type_id.name


    @api.depends('adults', 'child')
    def _compute_total_guests(self):
        for record in self:
            total_guests = record.adults + record.child
            record.total_guests = total_guests
            # if record.total_guest <= 
#===============================================================================
    @api.depends("guest_dob")
    def calculate_dob(self):
        for rec in self:
            if rec.guest_dob:
                today = datetime.date.today()
                age = today.year - rec.guest_dob.year - ((today.month, today.day) < (rec.guest_dob.month, rec.guest_dob.day))
                rec.age = age
                if age < 21:
                    raise ValidationError("You can't book the room, as the hotel.guest's age is below 21.")
#====================================================================================================
    # calculate total stay from check in date and check out date
    @api.depends('check_in_date','check_out_date',"stay")
    def _compute_days(self):
        for rec in self:
            if rec.check_in_date and rec.check_out_date:
                if rec.check_in_date < rec.check_out_date:
                    d= rec.check_out_date - rec.check_in_date
                    rec.stay= d.days
                    # rec.total_charge = rec.stay * rec.room_id.total_room_price

                else:
                    rec.stay = 0
            else:
                rec.stay=0

    @api.onchange('guest_id')
    def _onchange_guest_id(self):
        for rec in self:
            if rec.guest_id:
                rec.guest_photo = rec.guest_id.guest_photo
                rec.guest_phone = rec.guest_id.guest_phone
                rec.guest_gender = rec.guest_id.guest_gender
                rec.guest_dob = rec.guest_id.guest_dob 
                rec.identity_proof = rec.guest_id.identity_proof
                rec.identity_proof_number = rec.guest_id.identity_proof_number


#==========================================================================================
    @api.constrains('members_ids', 'adults', 'child')
    def _check_members(self):
        for record in self:
            # total_guests = record.adults + record.child
            no_of_members = len(record.members_ids)
            if self.total_guests > 1 and no_of_members < (self.total_guests - 1):
                raise ValidationError("You must add details for all members except the primary guest.")

    # ===============================================================================
    def get_available_rooms_filter(self, check_in_date, check_out_date):

        reservations = self.env['hotel.room.reservation'].search([
            ('check_in_date', '<=', check_out_date),
            ('check_out_date', '>=', check_in_date) 
        ])
        
        booked_rooms = reservations.mapped('room_id')
        booked_rooms_in_booking_lines = self.booking_lines_ids.mapped('room_id')
        all_rooms = booked_rooms + booked_rooms_in_booking_lines
        available_rooms = self.env['hotel.rooms'].search([
            ('id', 'not in', all_rooms.ids), 
            ('room_status', '=', 'available')   
        ])

        if self.room_id:
            available_rooms = available_rooms.filtered(lambda room: room.id != self.room_id.id)

        # If no available rooms are found, raise an error
        if not available_rooms:
            raise UserError("No available rooms found based on your preferences.")

        return available_rooms

#=====================================================================================
    def add_room(self):
        kanban_view_id = self.env.ref('hotel_management.hotel_room_available_view_kanban').id
        available_rooms_filter = self.get_available_rooms_filter(self.check_in_date, self.check_out_date)
       
        return {
            'name': 'Available Rooms',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.rooms',
            'view_mode': 'kanban',
            'views': [(kanban_view_id, 'kanban')],
            'domain': [('id', 'in', available_rooms_filter.ids), ('hotel_id', '=', self.hotel_id.id)],  # Show rooms in the selected hotel
            'target': 'current',
            'context': {'booking_id': self.id}
        }
#=================================================================
    def confirm_booking(self):
        self.status = 'confirm'
        self.room_status = 'occupied'
        self.room_id.reservation_id = self.id
#=================================================================
    def action_invoice(self):
        return {   
                    "type": "ir.actions.act_window",
                    "name": ("Customer Invoice"),
                    "view_mode": "form",
                    "res_model": "account.move",
                    "res_id": self.invoice_id.id,
                    "target": "current"}
#==================================================================
    def generate_invoice(self):
        if self.invoice_id:
            raise ValidationError("Invoice already created.....")
        if self.status == 'confirm':
            journal = self.env["account.journal"].search([('type', '=', 'sale')], limit=1)
            guest_id = self.env['res.partner'].create({
                    'name':self.guest_id.name
                })
            invoice_lines = []
            for booking_line in self.booking_lines_ids:
                invoice_lines.append(
                    Command.create({
                        'name': f"Room Charge ({booking_line.room_id.room_no})",
                        'quantity': self.stay,  
                        'price_unit': booking_line.amount,  
                    })
                )
            if booking_line.amount > 0:
                invoice_lines.append(
                    Command.create({
                        'name': "GST (18%)",
                        'quantity': 1,
                        'price_unit': 100,  
                    })
                )
            invoice = self.env["account.move"].create({
                'journal_id': journal.id,
                'move_type': 'out_invoice',  
                'partner_id': guest_id.id,
                'invoice_date': fields.Date.today(), 
                'invoice_line_ids': invoice_lines  
            })
            self.invoice_id = invoice.id
            return {   
                    "type": "ir.actions.act_window",
                    "name": ("Customer Invoice"),
                    "view_mode": "form",
                    "res_model": "account.move",
                    "res_id": invoice.id,
                    "target": "new"}
    
        else:
            raise ValidationError("You have to confirm your booking to generate invoice")
#=======================================================================================



