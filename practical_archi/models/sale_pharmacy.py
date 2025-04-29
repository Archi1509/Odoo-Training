from odoo import fields,api,models
from odoo.exceptions import ValidationError

class SalePharmacy(models.Model):
    _name = 'sale.pharmacy'
    _description = 'Pharmacy'

    name = fields.Char("Name")

    @api.constrains('name')
    def restrict_duplicate(self):
        for rec in self:
            existing_name = self.env['sale.pharmacy'].search([('name', '=', rec.name)])
            if existing_name:
                raise ValidationError("Pharmacy Names Cant be Same.")
