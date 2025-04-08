from email.policy import default

from odoo import fields,models,api
from odoo.exceptions import ValidationError


class HmsPrescription(models.Model):
    _name = "prescription.line"
    _description = "Prescription Line"
    _rec_name = "product_id"

    product_id=fields.Many2one('product.product',string="Product")
    qty=fields.Integer(string="Quantity",default=1)
    price_unit=fields.Float(string="Price")
    total=fields.Float(string="Total", compute="_compute_total")
    prescription_id = fields.Many2one("hms.prescription", string="Prescription", required=True, ondelete="cascade")
    move_ids=fields.One2many("stock.move","prescription_line_id","Delivery")


    @api.onchange('product_id')
    def onchange_fill_price(self):
        self.price_unit = self.product_id.lst_price or 10

    @api.depends('qty','price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total=rec.qty * rec.price_unit

    @api.constrains('qty')
    def check_quantity(self):
        for rec in self:
            qty_in_move=sum(rec.move_ids.mapped('product_uom_qty'))
            if rec.qty < qty_in_move:
                raise ValidationError("Quantity in Prescription cant be less then quantity in stock move")




