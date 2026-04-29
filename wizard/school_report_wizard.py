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
    class_ids = fields.Many2many('manage.class',string="Class")
    student_ids = fields.Many2many('registered.student',string="Student")
    date_from = fields.Date("From Date")
    date_to = fields.Date("To Date")
    filter_type = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('custom', 'Custom')
    ],default='month')
    club_ids = fields.Many2many('student.club',string="Club")
    department_ids = fields.Many2many('manage.department',string="Department")

    def action_print_report(self):
        report_action_type = self.report_type
        print(report_action_type)
        if report_action_type == 'student':
            if self.student_category == 'class' and not self.class_ids:
                self.class_ids = self.env['manage.class'].search([])
            elif self.student_category == 'department' and not self.department_ids:
                self.department_ids = self.env['manage.department'].search([])
            report_action = 'school_management.action_student_report'
        elif report_action_type == 'club':
            if not self.club_ids:
                self.club_ids = self.env['student.club'].search([])
            report_action = 'school_management.school_info_report'
        else:
            if self.leave_category == 'class' and not self.class_ids:
                self.class_ids = self.env['manage.class'].search([])
            elif self.leave_category == 'student' and not self.student_ids:
                self.student_ids = self.env['registered.student'].search([])
            report_action = 'school_management.student_leave_report'
        return self.env.ref(report_action).report_action(self)

