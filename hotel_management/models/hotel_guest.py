from datetime import datetime
from odoo.exceptions import ValidationError,UserError
from odoo import models, fields, api,_

class HotelGuest(models.Model):
    _name = 'hotel.guest'
    _description = 'Hotel Guest'
    _rec_name = 'name'

    guest_id = fields.Char(string="Guest ID", required=True, copy=False, readonly=False,
                            default=lambda self: _('New'))
    guest_photo = fields.Image(string="guest Photo",store=True)
    name =fields.Char(string="Guest Name", required=True)
    guest_phone = fields.Char(string="Mobile No.")
    guest_gender = fields.Selection([('male','Male'),
                                     ('female','Female')])
    guest_dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="calculate_dob", store=True)
    address = fields.Text(string="Address")
    email = fields.Char(string="Email")
    identity_proof = fields.Selection([('aadhar','Aadhar'),
                                       ('pan','Pan'),
                                       ('voter','Voter'),
                                       ('passport','Passport')],
                                       string="Identity Proof")
    identity_proof_number = fields.Char(string="Identity Proof Number")
    identity_proof_image = fields.Binary(string="Identity Proof Image")
    guest_member_ids = fields.Many2one('hotel.room.reservation', string="Member")

    @api.model
    def create(self, vals):
        if vals.get('guest_id', _('New')) == _('New'):
            vals['guest_id'] = self.env['ir.sequence'].next_by_code('hotel.guest') or _('New')  # Corrected field name
        return super().create(vals)
    

    @api.depends("guest_dob")
    def calculate_dob(self):
        for rec in self:
            if rec.guest_dob:
                today = datetime.today()
                age = today.year - rec.guest_dob.year - ((today.month, today.day) < (rec.guest_dob.month, rec.guest_dob.day))
                rec.age = age
                if age < 21:
                    raise ValidationError("You can't book the room, as the hotel.guest's age is below 21.")
