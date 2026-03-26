"""Student Register Model"""
# -*- coding: utf-8 -*-
from datetime import date
from odoo import fields, models, api


class RegisteredStudent(models.Model):
    """Registered Students Model"""
    _name = 'registered.student'
    _inherits = {'school.registration': 'registration_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = ' Registered Student'
    _rec_name = 'f_name'

    user_id = fields.Many2one('res.users', string='User',ondelete='cascade')
    registration_id = fields.Many2one(
        'school.registration',
        string='Registration',
        required=True,
        ondelete='cascade',
        auto_join=True
    )

    club_ids = fields.Many2many(
        'student.club',
        string="Clubs",
        ondelete='cascade'
    )

    current_class_id = fields.Many2one('manage.class', string='Current Class',
                                       compute="_compute_current_class",
                                       store=True)
    student_exam_id = fields.Many2many('student.exam', string='Exam', readonly=True)
    attendance = fields.Selection([('present', 'Present'),
                ('absent', 'Absent'),('half', 'Half Day')], default='present')

    @api.depends('registration_id.pre_class_id')
    def _compute_current_class(self):
        """Computing the next class based on previous class"""
        for record in self:
            prev_class = record.registration_id.pre_class_id
            if prev_class:
                next_class_number = str(int(prev_class.name) + 1)
                next_class = self.env['manage.class'].search([
                    ('name', '=', next_class_number)
                ], limit=1)
                record.current_class_id = next_class
            else:
                record.current_class_id = False

    def unlink(self):
        """Unlink the registered student from registration form
        Also unlink the corresponding user"""
        student_name = self.mapped('registration_id.f_name')
        parent_to_delete = self.mapped('registration_id')
        user_to_delete = self.env['res.users'].search([('name','in',student_name)])
        partner_to_delete = self.env['res.partner'].search([('name','in',student_name)])
        res = super(RegisteredStudent, self).unlink()
        parent_to_delete.unlink()
        if user_to_delete:
            user_to_delete.unlink()
        if partner_to_delete:
            partner_to_delete.unlink()
        return res


    def _user_creation(self):
        """Creating New User in the user model"""
        print("User Creation")
        for record in self:
            new_user = self.env['res.users'].create({
                "name": record.f_name,
                "login":record.email,
                "email":record.email,

            })
            new_user.partner_id.write({
                "role":'student'
            })
            record.user_id = new_user
        return new_user


    def daily_attendance_check(self):
        """Attendance Check based on leaves"""
        today = date.today()
        self.search([('attendance','in',['absent','half'])]).write({'attendance':'present'})
        leaves = self.env['school.leave'].search(['|',('start_date','=',today),'&',
                             ('start_date','<',today), ('end_date',">=",today)])
        for leave in leaves:
            student = leave.student_id
            if student.attendance == 'present':
                if leave.half_days:
                    student.write({'attendance':'half'})
                else:
                    student.write({'attendance':'absent'})
