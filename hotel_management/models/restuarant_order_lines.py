from odoo import models, fields,api,_

class RestaurantOrderLines(models.Model):
    _name = 'restaurant.order.lines'
    _description = 'Restaurant Order Lines'


    order_no = fields.Char(string="order", required=True, copy=False, readonly=False,
                            default=lambda self: _('New'))
    # order_no = fields.Char(string='Order Number')
    reservation_id = fields.Many2one('hotel.room.reservation', string="Reservation",ondelete='cascade')
    food_item_id = fields.Many2one('hotel.food.item', string="Food Item")
    quantity = fields.Integer(string="Quantity", default=1)
    price = fields.Float(string="Price")
    order_date = fields.Datetime(string="Order Date", default=fields.Datetime.now)
    status = fields.Selection(
        [('pending', 'Pending'), ('confirmed', 'Confirmed'), ('delivered', 'Delivered')],
        string="Order Status", default='pending'
    )

    @api.onchange('food_item_id')
    def _onchange_food_item_id(self):
        self.price = self.food_item_id.price

    @api.model
    def create(self, vals):
        if vals.get('order_no', _('New')) == _('New'):
            vals['order_no'] = self.env['ir.sequence'].next_by_code('restaurant.order.lines') or _('New')  # Corrected field name
        return super().create(vals)