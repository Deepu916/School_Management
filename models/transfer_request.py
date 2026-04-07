# -*- coding: utf-8 -*-
"""Transfer request model"""
from odoo import  fields, models,api



class TransferRequest(models.Model):
    """Transfer Request Model"""
    _name = "transfer.request"
    _description = "Transfer Request"
    _rec_name = 'student_id'

    student_id = fields.Many2one('registered.student',string="Student")
    student_class = fields.Char()
    current_company_id = fields.Many2one('res.company')
    new_company_id = fields.Many2one('res.company')
    state = fields.Selection([('approved','Approved'),('rejected','Rejected')])

    @api.onchange('student_id')
    def _onchange_name(self):
        if self.student_id:
            record = self.env['registered.student'].search([('id','=',self.student_id.id)])
            print(record, self.student_id)
            print(record.registration_id.company_id, record.company_id)
            self.student_class = record.current_class_id.name
            self.current_company_id = record.registration_id.company_id

    def action_confirm(self):
        """Confirm student Transfer"""
        self.state = 'approved'
        student = self.env['school.registration'].browse(self.student_id.id)
        student.write({'company_id':self.new_company_id})

    def action_reject(self):
        """Reject student Transfer"""
        self.state = 'rejected'
