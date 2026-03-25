"""School leave model"""
# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo.exceptions import ValidationError
from odoo import fields, models,api


class SchoolLeave(models.Model):
    """School Leave model"""
    _name = 'school.leave'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'School Leave'
    _rec_name = 'student_id'

    student_id = fields.Many2one('registered.student',string='Student',ondelete='cascade')
    student_class = fields.Char(string='Student Class')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    total_days = fields.Integer(compute='_compute_total_days', string='Total Days')
    half_days = fields.Boolean(string='Half Day')
    half_leave = fields.Selection([('forenoon','Forenoon'),('afternoon','Afternoon')],
                                  string='Half Leave')
    reason = fields.Text(string='Reason')

    @api.constrains('student_id','start_date','end_date','half_days','half_leave')
    def _check_same_time_leaves(self):
        """Prevent Duplicate student leave records"""
        for record in self:
            if record.half_days:
                duplicate = self.search([('student_id','=',record.student_id.id),
                                         ('half_days','=',True),
                                         ('half_leave','=',record.half_leave),
                                         ('start_date', '=', record.start_date),
                                         ('end_date', '=', record.end_date),
                                         ('id','!=',record.id)])
            else:
                duplicate = self.search([('student_id','=',record.student_id.id),
                                         ('half_days','=',False),
                                         ('start_date','=',record.start_date),
                                         ('end_date','=',record.end_date),
                                         ('id','!=',record.id)])
            if duplicate:
                raise ValidationError("The student already has a leave on that same time")


    @api.onchange('student_id')
    def _onchange_student(self):
        """Autofill  class when student is selected"""
        if self.student_id:
            record = self.env['registered.student'].search([('id','=',self.student_id.id)])
            self.student_class=record.current_class_id.name

    @api.depends('start_date','end_date')
    def _compute_total_days(self):
        """Computing total leave days excluding weekends """
        for record in self:
            if not record.end_date or not record.start_date:
                record.total_days = 0
                continue
            start=record.start_date
            end=record.end_date
            count=0
            while start<=end:
                if start.weekday()<5:
                    count+=1
                start+=timedelta(days=1)
            record.total_days=count
