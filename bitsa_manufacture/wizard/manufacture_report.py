from odoo import fields,api,models
import xlsxwriter
import io
import base64


class AddSerial(models.TransientModel):
    _name = 'manufacture.report'

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def download_manufacture_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Manufacturing Report')

        manufacture_data = self.env['mrp.production'].search([('date_start','>=',self.start_date),('date_finished','<=',self.end_date)])

        worksheet.write(0, 0, 'Product')
        worksheet.write(0, 1, 'Quantity')
        worksheet.write(0,2,'Schedule Date')


        row = 1
        for rec in manufacture_data:
            worksheet.write(row, 0, rec.product_id.name)
            worksheet.write(row, 1, rec.product_qty)
            worksheet.write(row, 2, rec.date_start.strftime('%Y-%m-%d %H:%M'))
            row += 1

        workbook.close()
        output.seek(0)

        attachment = self.env['ir.attachment'].create({
            'name': 'manufacturing_report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(output.read()),
            'res_model': 'manufacture.report',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'self',
        }
