from odoo import fields,api,models

class ApprovalTeams(models.Model):
    _name = 'approval.team'
    _description = 'Approval Team'

    name = fields.Char('Team Name')
    approval_levels = fields.One2many('team.approval.level','approval_team_id')