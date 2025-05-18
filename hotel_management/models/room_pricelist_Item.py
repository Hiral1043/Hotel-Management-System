from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError

class RoomPricelistItem(models.Model):
    _name = "room.pricelist.item"
    _description = "Room Pricelist Item"
    hotel_id = fields.Many2one('hotel.hotel')
    pricelist_id = fields.Many2one('hotel.pricelist', string="Pricelist")
    room_type_id = fields.Many2one('hotel.room.type', string="Room Type")
    price_type = fields.Selection([('discount',"Discount"),
                                   ('season','Season')])
    increase_price = fields.Float()
    season_id = fields.Many2one('hotel.season', string="Season")
    start_date = fields.Date(related='season_id.start_date', store=True)
    end_date = fields.Date(related='season_id.end_date' , store=True)   

    base_price = fields.Float(string="Base Price" ,related='room_type_id.price_per_night')

    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')
    ], string="Discount Type", default="fixed")

    discount_fixed = fields.Float(string="Fixed Discount")
    discount_percentage = fields.Float(string="Percentage Discount")
    final_price = fields.Float(string="Final Price", compute="_compute_final_price", store=True)

    

    @api.depends('base_price', 'discount_type', 'discount_fixed', 'discount_percentage')
    def _compute_final_price(self):
        for rec in self:
            if rec.price_type == 'discount':
                if rec.discount_type == 'fixed':
                    rec.final_price = rec.base_price - rec.discount_fixed
                elif rec.discount_type == 'percentage':
                    rec.final_price = rec.base_price - (rec.base_price * rec.discount_percentage / 100)
                else:
                    rec.final_price = rec.base_price
            
            elif rec.price_type == 'season':
                rec.final_price = rec.base_price + rec.increase_price
            else:
                rec.final_price = rec.base_price

    @api.onchange('price_type')
    def _onchange_price_type(self):
        for rec in self:
            if rec.price_type == 'season':
                rec.discount_fixed = 0.0
                rec.discount_percentage = 0.0
            elif rec.price_type == 'discount':
                rec.increase_price = 0.0
            else:
                rec.increase_price = 0.0
                rec.discount_fixed = 0.0
                rec.discount_percentage = 0.0
   
    @api.constrains('pricelist_id', 'room_type_id', 'start_date', 'end_date')
    def _check_unique_pricelist_item(self):
          for rec in self:
                record = self.search([
                 ('pricelist_id', '=', rec.pricelist_id.id),
                 ('room_type_id', '=', rec.room_type_id.id),
                 ('start_date', '=', rec.start_date),
                 ('end_date', '=', rec.end_date),
                ], limit=1)
                if record and record != rec:
                 raise ValidationError("A pricelist item with the same room type and date range already exists.")

            

