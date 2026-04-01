"""Student Club Model"""
# -*- coding: utf-8 -*-
from odoo import models, fields,api


class StudentClub(models.Model):
    """Student Club model"""
    _name = 'student.club'
    _description = 'School Club'

    name = fields.Char(string="Club Name", required=True)
    student_ids = fields.Many2many(
        'registered.student',
        relation='student_club_registered_student_rel',
        column1='club_id',
        column2='student_id',
        string="Students",
    )
    event_ids = fields.Many2many('club.event', string="Events",ondelete="cascade")
    event_count = fields.Integer(string="Events", compute="_compute_event_count")
    assigner_id = fields.Many2one('res.partner',string="Assigner",
                                  domain="[('role','=','teacher')]",ondelete="cascade")
    user_id = fields.Many2one('res.users',string="Students",)
    multi_school_id = fields.Many2one('res.company',
                    string="School", default=lambda self: self.env.user.company_id)

    @api.depends('event_ids')
    def _compute_event_count(self):
        """Compute number of events for the current club"""
        for record in self:
            record.event_count = len(record.event_ids)

    def action_event_count(self):
        """Stat Button Action """
        return {
            'name': 'Club Events',
            'type': 'ir.actions.act_window',
            'res_model': 'club.event',
            'view_mode': 'list,form',
            'domain': [('club_id', 'in', [self.id])],
        }
