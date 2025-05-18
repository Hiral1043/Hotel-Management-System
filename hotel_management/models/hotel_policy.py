from odoo import models,fields,api

class HotelPolicy(models.Model):
    _name = "hotel.policy"
    _description = 'Hotel Policy'

    name = fields.Char(string='Policy Name', required=True)  
    description = fields.Text(string='Policy Description', required=True) 
    policy_type = fields.Selection([
        ('check_in', 'Check-in Policy'),
        ('check_out', 'Check-out Policy'),
        ('cancellation', 'Cancellation Policy'),
        ('refund', 'Refund Policy')
    ], string="Policy Type", required=True) 
    hotel_id = fields.Many2one('hotel.hotel', string="Hotel")  
    reservation_id = fields.Many2one('hotel.room.reservation')
  