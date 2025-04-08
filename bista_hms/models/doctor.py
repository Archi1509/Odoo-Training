from odoo import fields,models,api
from datetime import datetime, timedelta

class ResDoctor(models.Model):
    _name = "res.doctor"
    _description = "Doctors"

    name=fields.Char(string="Name")
    specialization = fields.Many2one("hospital.specialization",string="Specialization")
    license_no = fields.Char(string="License Number" )
    experience_years = fields.Integer(string="Experience (Years)")
    hospital_id = fields.Many2one("hospital.hospital",string="Associated Hospital/Clinic")
    is_emergency_available = fields.Boolean(string="Emergency Available",default=True)
    email=fields.Char("Email")
    appointment_ids=fields.One2many("hms.appointment","doctor_id",string="Appointment")

    def action_send_email(self):
        template_id = self.env.ref('bista_hms.mail_template_appointment')
        res = self.env['hms.appointment'].search([])
        for record in res:
            template_id.send_mail(record.id,force_send=True)

    def send_appointment_mail(self):
        template_id = self.env.ref('bista_hms.mail_template_appointment')
        start_day = datetime.today().replace(hour=0, minute=0, second=1, microsecond=0)
        end_day = datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
        appointments=self.env['hms.appointment'].search([('appointment_date','<',end_day),('appointment_date','>',start_day),('state','=','confirm')])
        for app in appointments:
            template_id.send_mail(app.id, force_send=True)


