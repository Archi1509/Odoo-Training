from odoo import fields,models,api

class StagePercentage(models.Model):
    _name = "stage.percentage"
    _description = "Stage Percentage"
    _rec_name = "percentage"

    name = fields.Char("Name")
    percentage = fields.Float("Percentage")

