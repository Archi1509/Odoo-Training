from odoo import fields,models,api
from dateutil.relativedelta import relativedelta
from datetime import date,datetime


class Loan(models.Model):
    _name = 'bista.loan'
    _description = 'Loan Management System'
    _rec_name = 'partner_id'

    principal_loan_amount = fields.Float("Loan Amount")
    partner_id = fields.Many2one('res.partner',string="Partner",required=True)
    loan_tenure = fields.Integer('Loan Tenure(Loan Period)')
    interest_rates = fields.One2many('interest.rate','loan_id',string='Interest Rate')
    emi_lines = fields.One2many('emi.line','loan_id',string='Interest Rate')
    start_date = fields.Date('Loan Start Date')
    end_date = fields.Date('Loan End Date',compute='_compute_loan_end_date',store=True)#compute='_compute_loan_end_date',store=True
    emi_date = fields.Date('EMI Date')
    emi_amount = fields.Float('EMI Amount',compute='_compute_emi_amount',store=True)
    total_interest_amount = fields.Float('Total Interest Amount',compute='_compute_total_interest_amount',store=True)#,compute='_compute_total_interest_amount'
    paid_principal_amount = fields.Float('Paid Principal Amount',compute='_compute_total_interest_amount',store=True)
    pending_principal_amount = fields.Float('Pending Principal Amount',compute='_compute_total_interest_amount',store=True)
    user_id = fields.Many2one('res.users')
    rate = fields.Float("Current Rate",copy=False,compute='_compute_emi_amount',store=True)
    invoice_count=fields.Integer(string="Count",compute="_compute_related_invoice")
    invoice_ids = fields.One2many('account.move','loan_id',string='Invoice')
    next_emi_date = fields.Date('Next EMI Date',compute='_compute_next_emi_date',store=True)#,compute='_compute_next_emi_date'
    approval_levels = fields.One2many('loan.approval.level','loan_id',string='Approval Levels')
    approver_team = fields.Many2one('approval.team',string='Approver Team')
    next_approver = fields.Many2many('res.users',string='Next Approver',compute='_compute_get_next_approver',store=True)
    state = fields.Selection([('draft', 'Draft'),('to_approve','To Approve'),('approved','Approved'),('rejected','Rejected')],string="Status",default='draft')
    current_user_id = fields.Many2one('res.users',compute='_compute_current_user')

    def _compute_current_user(self):
        for rec in self:
            rec.current_user_id = self.env.user.id

    @api.depends('approval_levels')
    def _compute_get_next_approver(self):
        approver = []
        record = self.approval_levels.filtered(lambda rec:rec.stage == 'to approve')
        for rec in record:
            for id in rec.user_ids :
                approver.append(id.id)
        self.next_approver = [(6, 0, approver)]


    @api.onchange('approver_team')
    def link_approver_team(self):
        vals=[]
        self.approval_levels = [(5,0,0)]
        for rec in self.approver_team.approval_levels:
            vals.append((0, 0,({'level':rec.level,
                          'name':rec.name,
                          'user_ids':rec.user_ids})))
        self.approval_levels = vals
        for rec in self.approval_levels:
            if rec.stage == 'pending':
                rec.stage = 'to approve'
                break


    def action_confirm(self):
        self.state = 'to_approve'



    def action_to_approve(self):
        for record in self:
            approved = len(record.approval_levels.filtered(lambda rec: rec.stage == 'approved'))
            for rec in self.approval_levels:
                if rec.stage =='to approve':
                    rec.stage = 'approved'
                    rec.approved_by = self.env.user.name
                    rec.timestamp = datetime.now()

                if len(self.approval_levels) == approved + 1 :
                    record.state = 'approved'

                if rec.stage == 'pending':
                    rec.stage = 'to approve'
                    self._compute_get_next_approver()
                    break

    def action_reject(self):
        self.state = 'rejected'
        for rec in self.approval_levels:
            if rec.stage == 'to approve':
                rec.stage = 'rejected'
                rec.rejected_by = self.env.user.name
                rec.timestamp = datetime.now()

    @api.depends('paid_principal_amount')
    def _compute_next_emi_date(self):
        for rec in self:
            for line in rec.emi_lines:
                if line.state == 'pending':
                    rec.next_emi_date = line.date
                    break

    def _pay_emi_create_invoice(self):
        today =date.today()
        records = self.env['emi.line'].search([('date','=',today)])
        if records:
            for rec in records:
                 self.action_create_invoice(rec)
                 template = self.env.ref('bista_loan_management.loan_mail_template')
                 template.send_mail(self.id, force_send=True)


    def action_create_invoice(self,rec):
        invoice = self._prepare_invoice(rec)
        create_invoice = self.env['account.move'].create(invoice)
        emi_line=self.prepare_invoice_line_vals(create_invoice,rec)
        line_ids=self.env['account.move.line'].create(emi_line)
        create_invoice.action_post()
        rec.state = 'invoice generated'


    def _prepare_invoice(self,records):
        today = date.today()
        value = {
            'partner_id': records.loan_id.partner_id.id,
            'partner_shipping_id': records.loan_id.partner_id.id,
            'move_type':'out_invoice',
            'invoice_user_id': records.env.user.id,
            'company_id': records.env.user.company_id.id,
            'invoice_date': records.date,
            'user_id': records.env.user.id,
            'loan_id': records.loan_id.id,
        }
        return value

    def prepare_invoice_line_vals(self,create_invoice,rec):
        product_id = self.env['product.product'].search([('name','=','EMI2')])
        line_vals_list = []
        line_vals = {
            'product_id': product_id.id,
            'quantity': 1,
            'price_unit': rec.principal_paid,
            'discount': 0.0,
            'move_id': create_invoice.id,
            }
        line_vals_list.append(line_vals)
        return line_vals_list



    @api.depends('start_date', 'loan_tenure')
    def _compute_loan_end_date(self):
        for rec in self:
            if rec.start_date:
                month = rec.loan_tenure
                rec.end_date = rec.start_date + relativedelta(months=month)


    @api.depends('rate','principal_loan_amount','loan_tenure')
    def _compute_emi_amount(self):
        for rec in self:
            for line in self.emi_lines:
                if line.state == 'pending':
                    record = self.env['emi.line'].browse(line.id)
                    record.unlink()
            #EMI = [P * r * (1 + r)^N] / [(1 + r)^N - 1]
            paid_emi = len(self.emi_lines)
            p = rec.emi_lines[-1].balance if paid_emi else rec.principal_loan_amount
            monthly_rate = (rec.rate / 100) / 12
            n = rec.loan_tenure - paid_emi if paid_emi else rec.loan_tenure
            a = (1 + monthly_rate)**n
            b = a -1
            if b!=0:
                rec.emi_amount = p * (a * monthly_rate/b)
                rec.total_interest_amount = (rec.emi_amount * n) + rec.principal_loan_amount

    @api.depends('principal_loan_amount','emi_lines.state')
    def _compute_total_interest_amount(self):
        for rec in self:
            if rec.emi_amount:
                interests = sum(self.env['emi.line'].search([('loan_id','=',rec.id)]).mapped('interest_charged'))
                paid_principle = sum(self.env['emi.line'].search([('loan_id','=',rec.id),('state','=','invoice_paid')]).mapped('principal_paid'))
                rec.total_interest_amount = interests
                rec.paid_principal_amount = paid_principle
                rec.pending_principal_amount = rec.principal_loan_amount - paid_principle

    def action_calculate_emi_line(self):
        # create emi lines
        # EMI = [P * r * (1 + r)^N] / [(1 + r)^N - 1]
        monthly_rate = (self.rate / 1200)
        for rec in self.emi_lines:
            if rec.state == 'pending':
                record = self.env['emi.line'].browse(rec.id)
                record.unlink()

        paid_emi = len(self.emi_lines)
        n = paid_emi if paid_emi else 0
        vals = []
        emi_date = self.emi_lines[-1].date + relativedelta(months=1) if paid_emi else self.emi_date
        balance = self.emi_lines[-1].balance if paid_emi else self.principal_loan_amount

        for line in range(self.loan_tenure - n):
            interest_charged = monthly_rate * balance
            total_payment = self.emi_amount
            principal_paid = total_payment - interest_charged
            balance = balance - principal_paid
            vals.append((0, 0, ({
                    'principal_paid': principal_paid,
                    'interest_charged': interest_charged,
                    'total_payment': total_payment,
                    'date': emi_date,
                    'balance': balance,
                    'loan_id':self.id
                })))
            emi_date = emi_date + relativedelta(months=1)
        self.emi_lines = vals

    @api.depends('invoice_ids')
    def _compute_related_invoice(self):
        for record in self:
            record.invoice_count = self.env['account.move'].search_count(
                [('loan_id', '=', record.id)])

    def view_invoice(self):
        form_view_id = self.env.ref('account.view_move_form').id
        list_view_id = self.env.ref('account.view_out_invoice_tree').id

        res = {
            'name': 'Invoice',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'res_model':'account.move',
            'target': 'current',
            'view_id': list_view_id,
            'context': {'default_loan_id': self.id}
        }

        if self.invoice_count >= 0:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('loan_id', '=', self.id)]
            res['view_id'] = False
        return res













