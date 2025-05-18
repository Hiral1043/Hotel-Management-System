from odoo import models, fields, api, _

class Hotel(models.Model):
    _name = "hotel.hotel"
    _description = 'Hotel'
    _rec_name = 'hotel_name'

    reference = fields.Char(string="Hotel", required=True, copy=False, readonly=False,
                            default=lambda self: _('New'))
    hotel_name = fields.Char(string="Hotel Name")
    # print("\n\n\n\n\n\>>>>>>>>>",id)
    
    image = fields.Image()
    location = fields.Char(string="Location")
    landmarks = fields.Char(string="Landmarks")
    amenities_ids = fields.Many2many('hotel.amenities', string="Hotel Amenities") # this will link to amenities model
    policies_ids = fields.One2many('hotel.policy', 'hotel_id', string='Hotel Policies')  # Link to policy
    services_ids = fields.One2many('hotel.room.service', 'hotel_id', string='Hotel Services')
    room_ids = fields.One2many('hotel.rooms', 'hotel_id', string="Rooms")  # linked to rooms 
    
    ratings = fields.Selection(
        [('1', 'normal'), ('2', '2 star'), ('3', '3 star'),('4','4 star'),('5','5 star'),('7','7 star')],
        default='2'
    )

    def action_show_available_room(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Available Rooms',
            'view_mode': 'form',
            'res_model': 'available.room.wizard',
            'target': 'new',
            'context': {
                'default_hotel_id': self.id,
            },
        }
        
    @api.model
    def create(self, vals):
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hotel.hotel') or _('New')  # Corrected field name
        return super().create(vals)

    