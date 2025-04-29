from odoo import models,fields,api

class DocumentCustom(models.Model):
    _name = 'doc.tag.master'
    _description = "Custom Document System"

    name = fields.Char(string='Document Tag Name', required=True)

