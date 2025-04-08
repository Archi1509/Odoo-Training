from odoo import fields,models,api

class ResSpecialization(models.Model):
    _name = "hospital.specialization"
    _description = "Doctors Specialization"

    name=fields.Char(string="Name")
    des = fields.Text(string="Description")