"""Event Model"""
# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import  fields, models,api


class ClubEvent(models.Model):
    """Club event model"""
    _name = 'club.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Club Events'

    name = fields.Char(string='Event Name')
    description = fields.Text(string='Event Description')
    start_date = fields.Datetime(string='Start Date')
    end_date = fields.Datetime(string='End Date')
    club_id = fields.Many2many('student.club', string="Club",ondelete="cascade")
    state=fields.Selection([('planned','Planned'),('done','Done'),
                            ('cancelled','Cancelled')],default='planned')
    active = fields.Boolean(default=True)
    multi_school_id = fields.Many2one('res.company', string="School",
                        default=lambda self:self.env.user.company_id,required=True)

    def action_done(self):
        """Status done action"""
        self.state='done'

    def action_cancelled(self):
        """Status cancelled action"""
        self.state='cancelled'

    @api.model
    def _event_archive(self):
        """Archive events that have already occurred."""
        now=fields.Datetime.now()
        past_events = self.search([
            ('end_date', '<', now),
            ('active', '=', True)
        ])
        past_events.write({'active': False})

    @api.model
    def send_event_reminder(self):
        """ Send event reminder to all employees"""
        template = self.env.ref('school_management.email_template_remainder',
                                raise_if_not_found=False)
        if not template:
            return
        now = fields.Datetime.today() + timedelta(days=2)

        employees = self.env['res.partner'].search([('role', 'in', ['student', 'teacher', 'staff']),
                            ('email', '!=', False)])
        print(employees)

        if not employees:
            return
        main_email = employees[0]
        cc_emails = ','.join((employees - main_email).mapped('email'))
        upcoming_events = self.search([])
        if not upcoming_events:
            return
        event_names = [event.name for event in upcoming_events
                       if event.start_date.date() == now.date()]
        begin = upcoming_events[0].start_date.date()
        template.with_context(event_name=event_names,
                              date_begin=begin,
                              cc_emails=cc_emails).send_mail(main_email.id,
                              force_send=True,
                              email_values={'email_cc': cc_emails})
