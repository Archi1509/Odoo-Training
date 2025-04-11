from odoo import fields,models,api
class ProductProduct(models.Model):
    _inherit = "product.template"



    def action_update_onhand_product(self):
        view_id = self.env.ref('bista_hms.product_update_wizard_form').id
        return {
            'name': 'Update Quantity',
            'view_mode': 'form',
            'res_model': 'productupdate.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }


