from email.policy import default

from odoo import fields,models,api

class SaleRMA(models.Model):
    _name = "sale.rma"
    _description = "Sale RMA"
    _rec_name = "rma_id"

    rma_id = fields.Char(string="RMA ID",default="New")
    team_id = fields.Many2one("team.rma",string = "Team")
    date = fields.Date("Date")
    sale_order_id = fields.Many2one("sale.order", string = "Order")
    sale_rma_line = fields.One2many("sale.rma.line" , "sale_rma_id", string="RMAs")
    picking_ids = fields.One2many("stock.picking","rma_picking_id",string="Delivery")
    delivery_count=fields.Integer(string="Count",compute="_compute_count_deliveries")


    @api.onchange('sale_order_id')
    def link_sale_order_line(self):
        vals = []
        self.sale_rma_line = [(5,0,0)]
        for rec in self.sale_order_id.order_line:
            vals.append((0, 0, {
                'product_id': rec.product_id.id,
                'quantity': rec.product_uom_qty,
                'unit_price':rec.price_unit,
            }))
        self.sale_rma_line = vals

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
        rma_line =[]
        for line in self.sale_rma_line:
            rma_line.append((0,0,{
                'product_id':line.product_id.id,
                'sale_order_quantity':line.quantity,
                'quantity':line.to_receive,
            }))

        return {
            'name': 'Return',
            'view_mode': 'form',
            'res_model': 'rma.wizard',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':{'default_rma_line':rma_line}
        }
    def action_show_delivery(self):
        form_view_id = self.env.ref('stock.view_picking_form').id
        list_view_id = self.env.ref('stock.vpicktree').id

        res = {
            'name': 'Delivery',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'res_model': 'stock.picking',
            'target': 'current',
            'view_id': list_view_id,
            'context': {'default_rma_picking_id': self.id}
        }

        if self.delivery_count >= 0:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('prescription_id', '=', self.id)]
            res['view_id'] = False
        return res

    @api.depends('sale_rma_line.move_ids')
    def _compute_count_deliveries(self):
        for record in self:
            record.delivery_count = self.env['stock.move'].search_count([('rma_line_id', '=', record.id)])

