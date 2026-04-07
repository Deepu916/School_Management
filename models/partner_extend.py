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

    def _user_creation_for_partner(self):
        """Create new user for partner"""
        if self.env.context.get('creating_user'):
            return
        for partner in self:
            if not partner.role:
                continue
            existing = self.env['res.users'].search([('partner_id','=',partner.id)], limit=1)
            if existing:
                continue
            if not partner.email:
                continue
            new_user = self.env['res.users'].with_context(creating_user=True).create({
                "name":partner.name,
                "email":partner.email,
                "login":partner.email,
                "partner_id":partner.id,

            })
            groups = {
                'student':'school_management.student_group',
                'teacher':'school_management.teacher_group',
                'staff':'school_management.staff_group',
            }
            group = self.env.ref(groups[partner.role])
            new_user.write({'group_ids':[(4,group.id)]})

    def write(self, vals):
        """Override this method to add new fields to partner model"""
        res = super().write(vals)
        if 'role' in vals and vals.get('role'):
            self._user_creation_for_partner()
        return res
