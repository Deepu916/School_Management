# -*- coding: utf-8 -*-

from odoo import  fields, models


class SchoolReportWizard(models.TransientModel):
    _name = "school.report.wizard"


    report_type = fields.Selection([
        ('leave', 'Leave'),
        ('club', 'Club'),
        ('student', 'Student')
    ],default = lambda self:self.env.context.get('report_type'))
    leave_category = fields.Selection([
        ('class','Class Wise'),
        ('student','Student Wise'),
    ],string='Report Category',default='class')
    student_category = fields.Selection([
        ('class','Class Wise'),
        ('department','Department Wise'),
    ],string='Report Category',default='class')
    class_id = fields.Many2one('manage.class',string="Class")
    student_id = fields.Many2one('registered.student',string="Student")
    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")
    filter_type = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('custom', 'Custom')
    ],default='month')
    club_id = fields.Many2one('student.club',string="Club")
    department_id = fields.Many2one('manage.department',string="Department")

    def action_print_report(self):
        report_action_type = self.report_type
        print(report_action_type)
        if report_action_type == 'student':
            report_action = 'school_management.action_student_report'
        elif report_action_type == 'club':
            report_action = 'school_management.school_info_report'
        # else:
        #     report_action = 'school_management.student_report'
        return self.env.ref(report_action).report_action(self)

