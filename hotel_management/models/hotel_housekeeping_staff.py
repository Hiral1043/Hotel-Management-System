from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class HotelHousekeepingStaff(models.Model):
    _name = 'hotel.housekeeping.staff'
    _description = 'Hotel Housekeeping Staff'
    _rec_name = 'name'

    name = fields.Char(string="Name", required=True)
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel")
    phone = fields.Char(string="Phone Number")
    email = fields.Char(string="Email")
    age = fields.Integer(string="Age")
    job_profile = fields.Char(string="Job profile")     
    identity_proof = fields.Selection([('aadhar', 'Aadhar'),
                                        ('pan', 'Pan'),
                                        ('voter', 'Voter'),
                                        ('passport', 'Passport')
                                    ], string="Identity Proof", required=True)
    identity_proof_number = fields.Char(string="Identity Proof Number", required=True)
    identity_proof_image = fields.Binary(string="Identity Proof Image")
    room_ids = fields.Many2many('hotel.rooms', string="Assigned Rooms")
    housekeeping_planning_ids = fields.Many2one('housekeeping.planning', string="Housekeeping Planning")    

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 18:
                raise ValidationError("Housekeeping staff must be at least 18 years old.")
            
    
