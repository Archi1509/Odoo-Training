from odoo import fields,models,api

class TeamRMA(models.Model):
    _name = "team.rma"
    _description = "Teams RMA"
    _rec_name = "team_name"

    team_name = fields.Char("Team Name")
    prefix = fields.Char("Prefix")


