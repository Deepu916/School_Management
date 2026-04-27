# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SchoolReportWizard(models.TransientModel):
    _name = "school.report.wizard"


    class_id = fields.Many2one('manage.class',string="Class")
    student_id = fields.Many2one('registered.student',string="Student")

