"""Department Model"""
# -*- coding: utf-8 -*-
from odoo import  fields, models


class ManageDepartment(models.Model):
    """Department managing model"""
    _name = 'manage.department'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Department'

    name = fields.Char(string="Department Name")
    hod_id = fields.Many2one('res.users', string="Head of the Department")
