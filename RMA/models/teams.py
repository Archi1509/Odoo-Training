from odoo import fields,models,api

class TeamRMA(models.Model):
    _name = "team.rma"
    _description = "Teams RMA"
    _rec_name = "team_name"

    team_id = fields.Char("Team",default="New")
    # team_id = fields.Many2one("team.rma",string = "Team")
    team_name = fields.Char("Team Name")


    @api.model_create_multi
    def create(self, vals_list):
        res = super(TeamRMA, self).create(vals_list)
        for record in res:
            record.team_id = self.env['ir.sequence'].next_by_code('team.rma')
        return res
