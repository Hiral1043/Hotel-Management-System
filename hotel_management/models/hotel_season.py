from odoo import models,fields,api

class HotelSeason(models.Model):
    _name = 'hotel.season'
    _description = 'Hotel Season'

    name = fields.Char(string="Season Name", required=True)
    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)
    non_refundable = fields.Boolean(string="Non Refundable", default=False)