from odoo import fields,models,api

class CrmLead(models.Model):
    _inherit = "crm.lead"

    product_ids = fields.Many2many("product.product",string="Product")
    stage_percentage = fields.Many2one("stage.percentage",string="Stage Percentage")


    def _prepare_opportunity_quotation_context(self):
        res = super(CrmLead,self)._prepare_opportunity_quotation_context()
        sale_order_line = []
        for product in self.product_ids:
            sale_order_line.append((0,0,{
                'product_id':product.id,
            }))
        res.update({'default_order_line': sale_order_line,
                    'default_stage_percentage':self.stage_percentage.id})
        return res




