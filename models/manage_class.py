"""Class Model"""
# -*- coding: utf-8 -*-
from odoo import fields, models


class ManageClass(models.Model):
    """ Class Managing model"""
    _name = 'manage.class'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Class'

    name = fields.Char(string="Class")
    department_id = fields.Many2one("manage.department")
    head_id = fields.Many2one( 'res.users', related='department_id.hod_id',
                               string="HOD", readonly=True,store=True)
    multi_school_id = fields.Many2one('res.company', string="School")
    student_ids = fields.One2many('registered.student','current_class_id',string="Student")
