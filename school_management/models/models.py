# -*- coding: utf-8 -*-
from odoo import fields,models


class School(models.Model):
    _name = 'school.details'
    _description = 'School Management System'

    name=fields.Char('School Name')
    fees=fields.Float("Fees")

