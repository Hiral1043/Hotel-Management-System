from odoo import models,fields,api

class HotelRoomSpecification(models.Model):
    _name = "hotel.room.specification"

    name = fields.Char(string = "Specification") 
