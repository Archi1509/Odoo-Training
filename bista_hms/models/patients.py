import typing
from datetime import date
from odoo import fields,models,api
from odoo.api import ValuesType
from odoo.exceptions import UserError

blood_group=[('A+','A+ve'),
             ('B+','B+ve'),
             ('O+','O+ve'),
             ('AB+','AB+ve'),
             ('A-','A-ve'),
             ('B-','B-ve'),
             ('O-','O-ve'),
             ('AB-','AB-ve')]

class ResPatient(models.Model):
    _name = 'res.patient'
    _description = 'Patient'

    patient_code = fields.Char(string="Patient ID",default='New')
    name=fields.Char(string='Name',required=True)
    age=fields.Char(string='Age',compute="_compute_calculate_age",store=True)
    blood_group=fields.Selection(blood_group,string='Blood Group',required=True)
    date_of_birth=fields.Date(string='Date Of Birth')
    previous_diseases=fields.Text(string='Previous Diseases')
    phone=fields.Char(string='Phone')
    email=fields.Char(string='Email')
    mobile=fields.Integer(string='Mobile')
    age_category=fields.Selection([('senior','Senior Citizen'),
                                   ('adult','Adult'),
                                   ('minor','Minor'),
                                   ('child','Child')])
    guardian_id=fields.Many2one('res.partner','Guardian')
    guardian_type=fields.Selection([('parent','Parent'),
                                    ('sibling', 'Sibling'),
                                    ('relative', 'Relative'),
                                    ('friend', 'Friend'),
                                    ('other', 'Other'),
                                    ])
    appointment_ids=fields.One2many('hms.appointment','patient_id',string='Patients')
    appointment_count=fields.Integer(string="Count",compute="_compute_action_appointment",store=True)
    weekly_visit=fields.Boolean(string="Weekly Visit")
    is_blocked=fields.Boolean(string="Is Blocked?")
    state=fields.Selection([('block','Block'),('unblock','Unblock')])
    partner_id=fields.Many2one("res.partner",string="Partner")

    @api.model_create_multi
    def create(self, data_list):
        details = super().create(data_list)
        for record in details:
            record.patient_code = self.env['ir.sequence'].next_by_code('res.patient')
        partner = self.env['res.partner'].create([{'name': details.name,
                                                   'phone': details.phone,
                                                   'email': details.email}])
        details.partner_id = partner.id
        return details


    @api.constrains('phone')
    def check_phone(self):
        if self.phone:
            for record in self:
                if record.phone and len(record.phone)<10:
                    raise UserError ("Phone Number should be minimum 10 digit")

            patient_ids=self.env['res.patient'].search_count([('phone','=', record.phone),('id','!=',record.id)])
            if patient_ids:
                raise UserError ("Phone number already exists")

    def action_open_appointments(self):
        view_id = self.env.ref('bista_hms.hms_appointment_form_view').id

        return {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hms.appointment',
            'view_id': view_id,
            'target': 'current',
            'context':{'default_patient_id':self.id,'child':True,'default_guardian_id':self.guardian_id,'default_guardian_type':self.guardian_type}
        }


    @api.depends('date_of_birth')
    def _compute_calculate_age(self):
        today=date.today()
        for record in self:
            if record.date_of_birth:
                years = today.year - record.date_of_birth.year
                months = today.month - record.date_of_birth.month
                days = today.day - record.date_of_birth.day
                record.age=str(years)+' years '+str(months)+' months '+str(days)+' days'
        return record

    @api.onchange('date_of_birth' ,'age')
    def select_age_category(self):
        if self.date_of_birth:
            for record in self:
                cal_age = date.today().year - record.date_of_birth.year
                if int(cal_age) > 60:
                    self.age_category = 'senior'
                elif int(cal_age) > 18:
                    self.age_category = 'adult'
                elif int(cal_age) > 10:
                    self.age_category = 'minor'
                elif int(cal_age) <= 10:
                    self.age_category = 'child'

    def _get_number_of_patient(self):
        print(self.env['res.patient'].search_count([('date_of_birth', '<=', date.today().replace(year=date.today().year - 40))]))


    @api.depends('appointment_ids.patient_id')
    def _compute_action_appointment(self):
        for record in self:
            record.appointment_count=self.env['hms.appointment'].search_count([('patient_id','in',record.ids)])





    def action_get_appointment_count(self):
        form_view_id = self.env.ref('bista_hms.hms_appointment_form_view').id
        list_view_id = self.env.ref('bista_hms.hms_appointment_list_view').id

        res = {
            'name': 'Appointments',
            'type': 'ir.actions.act_window',
            'view_mode': 'list',
            'res_model': 'hms.appointment',
            'target': 'current',
            'view_id': list_view_id,
            'context': {'default_patient_id': self.id}
        }

        if self.appointment_count >= 1:
            res['view_mode'] = 'list,form'
            res['views'] = [(list_view_id, 'list'), (form_view_id, 'form')]
            res['domain'] = [('patient_id', '=', self.id)]
            res['view_id'] = False

        return res

    @api.model
    def _weekly_visit_action(self):
        appointments=self.env['res.patient'].search([('weekly_visit','=',True)])
        for patients in appointments:
            self.env['hms.appointment'].create([{
                'patient_id':patients.id,
                'phone':patients.phone
            }])
        print(appointments)

    def block_user(self):
        self.is_blocked = True
        self.state='block'

    def unblock_user(self):
        self.is_blocked = False
        self.state='unblock'



    def write(self, vals):
        if self.env.context.get('prevent_recursive_write_patient'):
            return super(ResPatient, self).write(vals)
        for patient in self:
            if patient.partner_id:
                partner_vals = {}
                if 'name' in vals:
                    partner_vals['name'] = vals['name']
                if 'phone' in vals:
                    partner_vals['phone'] = vals['phone']
                if 'mobile' in vals:
                    partner_vals['mobile'] = vals['mobile']
                if 'email' in vals:
                    partner_vals['email'] = vals['email']
                patient.partner_id.with_context(prevent_recursive_write_patient=True).write(partner_vals)

        if "phone" in vals:
            if len(vals.get("phone")) < 10 or len(vals.get("phone")) > 10:
                raise UserError("Enter 10 Digit Number")

        for record in self:
            if record.is_blocked and 'is_blocked' not in vals:
                raise UserError("Blocked patient cannot edit their details.")
        res=super().write(vals)
        return res






