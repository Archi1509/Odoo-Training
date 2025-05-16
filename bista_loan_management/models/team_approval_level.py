from odoo import fields,api,models


class TeamApprovalLevel(models.Model):
    _name = 'team.approval.level'
    _description = 'Approval Levels'

    level = fields.Integer('Team Name',compute='_compute_level',store=True,readonly=True)
    name = fields.Char('Name')
    user_ids = fields.Many2many('res.users')
    # stage = fields.Selection([('pending','Pending'),('to approve','To Approve'),('approved','Approve'),('rejected','Rejected')])
    # approved_by = fields.Char(string='Approved By')
    # rejected_by = fields.Char(string='Rejected By')
    # timestamp = fields.Datetime('Timestamp')
    loan_id = fields.Many2one('bista.loan',string='Loan')
    approval_team_id = fields.Many2one('approval.team',string='Team')

    @api.depends('approval_team_id.approval_levels')
    def _compute_level(self):
        for rec in self:
            l = 0
            rec.level = l
            for no in rec.approval_team_id.approval_levels:
                l += 1
                no.level = l
        return






