from odoo import models, fields, api

class HousekeepingCheckList(models.Model):
    _name = 'housekeeping.check.list'
    _description = 'Housekeeping Check List'

    name = fields.Char(string='Services', required=True)
   