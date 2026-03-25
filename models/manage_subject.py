"""Subject Model"""
# -*- coding: utf-8 -*-
from odoo import fields, models


class ManageSubject(models.Model):
    """Subject managing model"""
    _name = 'manage.subject'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Subject'

    name = fields.Char(string="Subject Name")
    department_id = fields.Many2many(comodel_name='manage.department')
