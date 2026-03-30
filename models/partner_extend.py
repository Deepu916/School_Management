"""Inherit Partner"""
# -*- coding: utf-8 -*-
from odoo import  fields, models


class PartnerExtend(models.Model):
    """Adding New Field to partner model"""
    _inherit = "res.partner"

    role = fields.Selection([('student','Student'),('teacher','Teacher'),
                             ('staff','Office Staff')],string="Role")
    student_id = fields.Many2one('registered.student',string="Student")
    _unique_partner_role = models.Constraint('UNIQUE(name,role)',
                                'A partner with this name and role already exists')
