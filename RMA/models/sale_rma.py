from odoo import fields,models,api

class SaleRMA(models.Model):
    _name = "sale.rma"
    _description = "Sale RMA"
    _rec_name = "rma_id"

    rma_id = fields.Char(string="RMA ID",default="New")
    team_id = fields.Many2one("team.rma",string = "Team")
    date = fields.Date("Date")
    sale_order = fields.Many2one("sale.order", string = "Order")
    sale_rma_line = fields.One2many("sale.rma.line" , "sale_rma_id", string="RMAs")

    @api.model_create_multi
    def create(self, vals_list):
        res = super(SaleRMA, self).create(vals_list)
        for record in res:
            if record.rma_id == "New":
                base_seq = self.env['ir.sequence'].next_by_code('sale.rma')
            else:
                base_seq = record.rma_id

            team_order = self.env['team.rma'].search([('team_name','=',record.team_id.team_name)],limit=1)
            suffix = team_order.team_id if team_order  else "Unknown"

            record.rma_id = f'{base_seq}/{suffix}'

        return res

    def action_open_wizard(self):
        view_id = self.env.ref('RMA.rma_wizard_form').id
        return {
            'name': 'product_id',
            'view_mode': 'form',
            'res_model': 'rma.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    
