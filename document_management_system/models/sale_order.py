from docutils.nodes import document

from odoo import fields,api,models
from odoo.api import readonly


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tags_ids = fields.Many2many(
        'doc.tag.master',
        string='Doc Tag')
    document_ids = fields.Many2many('document.custom',string='Documents')
    document_count = fields.Integer("Documents Count",compute="_compute_count_document",store=False)
    document_lines = fields.One2many("sale.order.document.line",'sale_order_doc_line',string='Document')
    show_update_button = fields.Boolean(compute ='_compute_get_system_parameter')



    @api.onchange('partner_id')
    def get_tags(self):
        if self.partner_id:
            self.tags_ids = self.partner_id.tag_ids

    def action_get_document(self):
        docs = self.env['document.custom']
        for line in self.order_line:
            product = line.product_template_id
            docs  |= product.product_variant_id.document_ids.filtered(lambda doc: any(tag in self.tags_ids for tag in doc.tag_ids))
        self.document_ids =[(6,0,docs.ids)]

        #this is for sending email on button click
        if self.user_id and self.user_id.login:
            template = self.env.ref('document_management_system.dms_mail_template')
            template.send_mail(self.id, force_send=True)

        #This Part is for Document Lines
        lines_dict = {}
        self.document_lines = [(5, 0, 0)]  # Clear existing lines

        for doc in self.document_ids:
            for product in self.order_line:
                if doc in product.product_id.document_ids:
                    if doc.id in lines_dict:
                        lines_dict[doc.id].add(product.product_id.id)
                    else:
                        lines_dict[doc.id] = {product.product_id.id}

        lines = []
        for doc_id, prod_ids in lines_dict.items():
            lines.append((0, 0, {
                'document_id': doc_id,
                'product_ids': [(6, 0, list(prod_ids))]
            }))

        self.document_lines = lines

    def action_update_document(self):
        self.ensure_one()
        if self.state != 'sale':
            return
        existing_docs = self.document_ids
        new_docs = self.action_get_document()
        print(existing_docs)
        print(new_docs)
        if new_docs:
            added_docs = new_docs.filtered(lambda doc: doc not in existing_docs)
            if added_docs:
                for picking in self.picking_ids:
                    picking.document_ids |= added_docs
        self.message_post(body=f"Hi, This order is created by {self.env.user.name}.")


    def action_confirm(self):
        super().action_confirm()
        self.picking_ids.document_ids = self.document_ids

    @api.depends('document_ids')
    def _compute_count_document(self):
        for rec in self:
            rec.document_count = len(rec.document_ids)

    def _compute_get_system_parameter(self):
        for rec in self:
            allowed_update = self.env['ir.config_parameter'].sudo().get_param('sale.update_document_button')
            if allowed_update == '0':
                rec.show_update_button = False
            else:
                rec.show_update_button = True

    def action_open_wizard(self):
        view_id = self.env.ref('document_management_system.add_document_wizard_form').id
        return {
            'name': 'Add Products',
            'view_mode': 'form',
            'res_model': 'add.product',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context':{'default_sale_order':self.id}
        }












