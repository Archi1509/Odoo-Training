from odoo import fields,models,api
from odoo.exceptions import ValidationError


class HmsPrescription(models.Model):
    _name = "hms.prescription"
    _description = "Prescription"
    _rec_name = "patient_id"
    _inherit = ['mail.thread','mail.activity.mixin']

    patient_id=fields.Many2one('res.patient',string="Patient")
    date=fields.Date(string="Date", tracking=True)
    doctor_id=fields.Many2one("res.doctor",string="Doctor")
    medicines = fields.Text(string="Medicines")
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft',tracking=True)
    prescription_lines=fields.One2many("prescription.line","prescription_id",string="Prescription" )
    prescription_count=fields.Integer(string="Count",compute="_compute_related_prescription")
    total_amount = fields.Float(compute='_compute_total_amount', string="Total Amount",store=True)
    invoice_id=fields.Many2many("account.move",string="Invoice")
    picking_ids=fields.One2many("stock.picking","prescription_id","Pickings")
    delivery_count=fields.Integer(string="Count",compute="_compute_count_deliveries")
    previous_delivery_quantity=fields.Integer("Previous Quantity")

    def action_print_report(self):
        template_id = self.env.ref('bista_hms.action_prescription_report')
        return template_id.report_action(self)

    @api.depends('prescription_lines.move_ids')
    def _compute_count_deliveries(self):
        for record in self:
            record.delivery_count=self.env['stock.move'].search_count([('prescription_line_id','=',record.id)])

    def action_create_delivery(self):
        picking_vals=self.prepare_picking_vals()
        picking_id = self.env['stock.picking'].create(picking_vals)

        move_vals=self.prepare_move_vals(picking_id)
        move_id=self.env['stock.move'].create(move_vals)

    def prepare_picking_vals(self):
        picking_type_id=self.env['stock.picking.type'].search([('code','=','outgoing')])
        vals={
            'partner_id':self.patient_id.partner_id.id,
            'picking_type_id':picking_type_id.id,
            'location_dest_id':picking_type_id.default_location_dest_id.id,
            'location_id':picking_type_id.default_location_src_id.id,
            'origin':self.display_name,
            'prescription_id':self.id
        }
        return vals

    def prepare_move_vals(self,picking_id):
        move_vals=[]
        for line in self.prescription_lines:
            if line.move_ids:
                continue
            qty_in_move = sum(line.move_ids.mapped('product_uom_qty'))
            to_deliver = line.quantity - qty_in_move
            vals={
                    'picking_type_id':picking_id.picking_type_id.id,
                    'location_id':picking_id.location_id.id,
                    'location_dest_id':picking_id.location_dest_id.id,
                    'picking_id':picking_id.id,
                    'product_id':line.product_id.id,
                    'name':line.product_id.display_name,
                    'product_uom_qty':to_deliver,
                    'prescription_line_id':line.id
                }
            move_vals.append(vals)
        return move_vals

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
            'context': {'default_prescription_id': self.id}
        }

        if self.delivery_count >= 0:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('prescription_id', '=', self.id)]
            res['view_id'] = False
        return res

    def action_confirm(self):
        self.state = 'confirm'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('prescription_lines.product_id')
    def _compute_related_prescription(self):
        for record in self:
            record.prescription_count=self.env['prescription.line'].search_count([('prescription_id','=',record.id)])

    def view_prescription(self):
        form_view_id = self.env.ref('bista_hms.line_view_form').id
        list_view_id = self.env.ref('bista_hms.line_view_list').id

        res={
            'name': 'Prescriptions',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'res_model': 'prescription.line',
            'target': 'current',
            'view_id': list_view_id,
            'context': {'default_prescription_id': self.id}
        }

        if self.prescription_count >= 0:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('prescription_id', '=', self.id)]
            res['view_id'] = False
        return res

    @api.depends('prescription_lines.total')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(rec.prescription_lines.mapped('total'))

    def action_create_invoice(self):
        if not self.prescription_lines:
            raise ValidationError("Please add prescription lines before creating an invoice.")
        invoice = self._prepare_invoice()
        create_invoice = self.env['account.move'].create(invoice)
        product_prescription_line=self.prepare_invoice_line_vals(create_invoice)
        line_ids=self.env['account.move.line'].create(product_prescription_line)
        print(create_invoice)
        return create_invoice

    def _prepare_invoice(self):
        value = {
            'partner_id': self.patient_id.partner_id.id,
            'partner_shipping_id': self.patient_id.partner_id.id,
            'move_type':'out_invoice',
            'invoice_user_id': self.env.user.id,
            'company_id': self.env.user.company_id.id,
            'invoice_date': self.date,
            'user_id': self.env.user.id,
        }
        return value

    def prepare_invoice_line_vals(self,create_invoice):
        line_vals_list = []
        for line in self.prescription_lines:
            line_vals = {
                'product_id': line.product_id.id,
                'quantity': line.qty,
                'price_unit': line.price_unit,
                'discount': 0.0,
                'move_id': create_invoice.id,
            }
            line_vals_list.append(line_vals)
        return line_vals_list




