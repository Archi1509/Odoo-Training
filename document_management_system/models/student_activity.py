from odoo import fields,models

class School(models.Model):
    _name = 'student.activity'
    _description = 'Student Activity'

    name=fields.Char('School Name')
    fees=fields.Float("Fees")
    address = fields.Char("Address")

