from odoo import fields,models,api

class ResSpecialization(models.Model):
    _name = "hospital.hospital"
    _description = "Hospital"

    name=fields.Char(string="Name")
    des = fields.Text(string="Description")