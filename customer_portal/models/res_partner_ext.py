from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    username = fields.Char(string='Username', required=True, unique=True)
    password = fields.Char(string='Password', required=True)
