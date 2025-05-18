from odoo import models,fields,api

class HotelPricelist(models.Model):
    _name = 'hotel.pricelist'
    _description = 'Hotel Pricelist'

    name = fields.Char(string="Price list")
    item_ids = fields.One2many('room.pricelist.item', 'pricelist_id', string='Price Rules')
    # hotel_id = fields.Many2one('hotel.hotel')
