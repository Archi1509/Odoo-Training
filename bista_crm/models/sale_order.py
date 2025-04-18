from itertools import product

from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    stage_percentage = fields.Many2one("stage.percentage",string="Stage Percentage")

    def action_confirm(self):
        super().action_confirm()
        select_stage = self.env['stage.percentage'].search([('percentage','=',100)])
        if not self.stage_percentage:
            if not select_stage:
                raise ValidationError("Select a Stage.")
            else:
                self.stage_percentage = select_stage





