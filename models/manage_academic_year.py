"""Academic year model"""
# -*- coding: utf-8 -*-
from odoo import fields, models


class ManageAcademicYear(models.Model):
    """ Academic Year Managing model """
    _name = 'manage.academic'
    _description = 'Academic Year'

    name = fields.Char(string="Academic Year")
