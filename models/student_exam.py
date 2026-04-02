"""Student exam model"""
# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class StudentExam(models.Model):
    """Student exam model"""
    _name = 'student.exam'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Student Exam'

    name = fields.Char(string='Exam Name')
    class_name_id = fields.Many2one('manage.class', string='Class')
    class_department_id = fields.Many2one('manage.department',
                                          related='class_name_id.department_id',
                                          string='Department')
    state = fields.Selection(
        [('draft', 'Draft'), ('assigned', 'Assigned')],
        default='draft'
    )
    paper_line_ids = fields.One2many(
        'student.exam.paper_line', 'exam_id', string='Exam Papers'
    )
    student_id = fields.Many2many('registered.student', string='Student', ondelete='cascade')
    company_id = fields.Many2one('res.company',
                    string="School", default=lambda self: self.env.user.company_id)

    def action_add(self):
        """Assigning  Exam to Student button action"""
        if self.state == 'draft':
            students = self.env['registered.student'].search([
                ('current_class_id', '=', self.class_name_id.id)])

            if not students:
                raise UserError('No student registered with this class')
            for student in students:
                student.write({'student_exam_id': [(4, self.id)]})
                print(student)
            self.state = 'assigned'


class StudentExamPaperLine(models.Model):
    """Student exam paper line"""
    _name = 'student.exam.paper_line'
    _description = 'Student Exam Paper Line'

    exam_id = fields.Many2one('student.exam', string='Exam', readonly=True)

    subject_department_id = fields.Many2one(
        'manage.department',
        related='exam_id.class_department_id',
        store=True
    )
    subject_id = fields.Many2one('manage.subject', string='Subject',
                                 domain="['|', ('department_id', '=', False),"
                                        "('department_id', '=', subject_department_id)]")
    pass_mark = fields.Float(string='Pass Mark')
    max_mark = fields.Integer(string='Max Mark')
