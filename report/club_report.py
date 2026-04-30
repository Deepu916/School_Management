# -*- coding: utf-8 -*-
from odoo import models


class ClubReport(models.AbstractModel):
    _name = 'report.school_management.school_report_template'


    # def _get_report_values(self,docids, data):
    #     docs = self.env['school.report.wizard'].browse(docids)
    #     return ({
    #         'doc_ids': docids,
    #         'doc_model': 'school.report.club_report',
    #         'docs': docs,
    #         'data': data,
    #     })
