import datetime
from datetime import datetime, timedelta
from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError


class HmsAppointment(models.Model):
    _name = "hms.appointment"
    _description = "Appointment"
    _rec_name = 'patient_id'

    appointment_code = fields.Char(string="Appointment ID")
    phone = fields.Char(string="Phone")
    patient_id=fields.Many2one("res.patient",string='Patient',required='True')
    appointment_date=fields.Datetime(string='Date',required=True,default=datetime.now()+timedelta(hours=1))
    appointment_reason=fields.Text(string='Reason')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirm', 'Confirm'),
                              ('waiting', 'Waiting'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancel', 'Cancel')],
                             string="Status", default='draft')
    consultation_start=fields.Datetime(string="Consultation Start" ,default=datetime.now())
    consultation_end=fields.Datetime(string="Consultation End",default=datetime.now())
    total_time=fields.Float(string="Total Time")
    guardian_id=fields.Many2one('res.partner','Guardian')
    guardian_type=fields.Selection([('parent','Parent'),
                                    ('sibling', 'Sibling'),
                                    ('relative', 'Relative'),
                                    ('friend', 'Friend'),
                                    ('other', 'Other'),
                                    ])
    product = fields.Many2one('product.product', string="Product")
    doctor_id=fields.Many2one("res.doctor",string="Doctor")




    @api.model_create_multi
    def create(self, data_list):
        res=super(HmsAppointment,self).create(data_list)
        for record in res:
            record.appointment_code = self.env['ir.sequence'].next_by_code('hms.appointment')
        return res

    @api.constrains('appointment_date')
    def check_appointment_date(self):
        today=datetime.now()
        for record in self:
            if record.appointment_date<today:
                raise UserError ("Select Future Dates")

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.phone = self.patient_id.phone
            self.guardian_id = self.patient_id.guardian_id
            self.guardian_type = self.patient_id.guardian_type

    def _send_appointment_reminder_today(self):
        # Send appointment reminder to patients
        # This method will be called by a cron job
        start_day = datetime.today().replace(hour=0, minute=0, second=1, microsecond=0)
        end_day = datetime.today().replace(hour=23, minute=59, second=59, microsecond=0)
        appointment_ids = self.env['hms.appointment'].search([('appointment_date', '>=', start_day),
                                                              ('appointment_date', '<=', end_day),])

    def _weekly_consultation_report(self):
        week_day = datetime.now() - timedelta(days=7)
        dict={}
        patient=[]
        appointments=self.env['hms.appointment'].search([('consultation_start', '>=', week_day), ('consultation_start', '<=', datetime.now())])
        number_of_appointments=len(appointments)
        total_consultation_time=0.00
        for record in appointments:
            total_consultation_time += record.total_time
            if record.total_time>1:
                patient.append(record.patient_id.name)
        dict["Number of Appointments"]=number_of_appointments
        dict["Total Consultation Time"] = total_consultation_time
        dict["Patients"] = patient
        print(dict)

    def action_confirm(self):
        self.state = 'confirm'

    def action_in_consultation(self):
        self.state = 'in_consultation'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancel'

    def action_waiting(self):
        self.state = 'waiting'

    @api.onchange('consultation_start', 'consultation_end')
    def _calculate_total_time(self):
        for record in self:
            if record.consultation_start and record.consultation_end:
                delta = record.consultation_end - record.consultation_start
                record.total_time = delta.total_seconds()/3600 # Convert to hours
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(delta)


    @api.constrains('patient_id', 'appointment_date')
    def restrict_duplicate_appointment(self):
        for rec in self:
            existing_appointment = self.env['hms.appointment'].search([
                ('patient_id', '=', rec.patient_id.id),
                ('appointment_date', '=', rec.appointment_date),
                ('id', '!=', rec.id)
            ])
            if existing_appointment:
                raise ValidationError("A patient cannot have two appointments on the same day.")


    def _weekly_cancellation_report(self):
        week_day = datetime.now() - timedelta(days=7)
        report_list = []

        for rec in self.search([('state', '=', 'cancel'), ('consultation_start', '>=', week_day), ('consultation_start', '<=', datetime.now())]):
            report_list.append({
                "Appointment Number": rec.appointment_code,
                "Patient": rec.patient_id.name,
                "Date of Appointment": rec.appointment_date
            })

        print("Weekly Cancellation Report:", report_list)
        return report_list


    def _auto_cancellation(self):
        time_limit = fields.Datetime.now() - timedelta(hours=24)
        for record in self.search([('state','=','draft'),('appointment_date','>',time_limit)]):
            record.state='cancel'









