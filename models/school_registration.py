"""School registration model"""
# -*- coding: utf-8 -*-
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import fields, models, api


class SchoolRegistration(models.Model):
    """School registration model"""
    _name = 'school.registration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Student Registration'
    _check_company_auto = True
    _rec_name = 'sequence'


    f_name = fields.Char(string="First Name", required=True, tracking=True,ondelete="cascade")
    l_name = fields.Char(string="Last Name", required=True, tracking=True)
    father = fields.Char(string=" Father's Name")
    mother = fields.Char(string=" Mother's Name")
    communication_address = fields.Text(string="Communication Address")
    street = fields.Char(string="Street Address")
    street2 = fields.Char(string="Street Address 2")
    city = fields.Char(string="City")
    country_id = fields.Many2one('res.country')
    state_id = fields.Many2one('res.country.state', 'Fed.state')
    zip = fields.Char(string="Zip")
    same_as_communication = fields.Boolean(default=False)
    permanent_address = fields.Text(string="Permanent Address")
    prem_street = fields.Char(string="Street Address")
    prem_street2 = fields.Char(string="Street Address 2")
    prem_city = fields.Char(string="City")
    prem_country_id = fields.Many2one('res.country')
    prem_state_id = fields.Many2one('res.country.state', 'Fed.state')
    prem_zip = fields.Char(string="Zip")
    email = fields.Char(string="Email", tracking=True,copy=False,required=True)
    phone = fields.Char(string="Phone", tracking=True,copy=False)
    dob = fields.Date(string="DOB")
    age = fields.Integer(compute='_compute_age', string="Age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'),
                               ('other', 'Other')], string="Gender",copy=False)
    registration_date = fields.Date(default=lambda self: fields.Date.today(),copy=False)
    image = fields.Image(string="Image")
    pre_academic_dpt = fields.Selection([('lp', 'LP'), ('up', 'UP'),
                     ('hs', 'HS')],string="Previous Academic Department",copy=False)
    pre_class_id = fields.Many2one('manage.class', string="Previous Class",copy=False)
    tc = fields.Binary(string="TC", attachment=True)
    aadhaar_number = fields.Char(string="Aadhaar Number", tracking=True,copy=False)
    sequence = fields.Char(string='Sequence', copy=False, default="New", readonly=True)
    status = fields.Selection([('draft', 'Draft'), ('registered', 'Registered')], default="draft")
    admission_number = fields.Char(string="Admission Number",readonly=True,copy=False)
    company_id = fields.Many2one('res.company', string="School",
                                      default=lambda self:self.env.user.company_id)
    user_ids = fields.Many2one('registered.student',string="User",ondelete='cascade')


    _aadhaar_unique = models.Constraint('UNIQUE(aadhaar_number)','Aadhaar number must be unique')


    @api.depends('dob')
    def _compute_age(self):
        """Compute Age"""
        for record in self:
            if record.dob:
                today = date.today()
                difference = relativedelta(today, record.dob)
                record.age = difference.years
            else:
                record.age = 0

    @api.model_create_multi
    def create(self, vals_list):
        """Unique register number generation and admission number generation"""
        for vals in vals_list:
            if vals.get('sequence', 'New') == 'New':
                vals['sequence'] = self.env['ir.sequence'].next_by_code('sequence_code') or 'New'
        records = super().create(vals_list)
        for record in records:
            if record.status == 'registered':
                record.admission_number = self.env['ir.sequence'].next_by_code('student_admission')
                record._create_registered_student()
        return records

    def action_register(self):
        """Register Button Action for status change and creating registered record"""
        if self.status == 'draft':
            self.write({'status': 'registered',
            'admission_number':self.env['ir.sequence'].next_by_code('student_admission')})
            self._create_registered_student()

    def _create_registered_student(self):
        """Create registered student record"""
        existing = self.env['registered.student'].search(
            [('registration_id', '=', self.id)], limit=1)
        if not existing:
            self.env['registered.student'].create({'registration_id': self.id,})
            self.user_ids = self.env['registered.student'].search([('registration_id','=',self.id)])


    def action_sync_exam(self):
        """Sync exam records for new registered students"""
        registered = self.env['registered.student'].search(
            [('registration_id', '=', self.id)], limit=1)
        exams = self.env['student.exam'].search([
            ('class_name_id', '=', registered.current_class_id.id),
            ('state', '=', 'assigned')
        ])
        for exam in exams:
            registered.write({'student_exam_id': [(4, exam.id)]})
