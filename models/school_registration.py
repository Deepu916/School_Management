from odoo import fields, models,api


class Registration(models.Model):
    _name = 'school.management.registration'

    f_name = fields.Char(string="First Name",required=True)
    l_name = fields.Char(string="Last Name",required=True)
    father = fields.Char(string=" Father's Name")
    mother = fields.Char(string=" Mother's Name")
    communication_address = fields.Text(string="Communication Address")
    street=fields.Char(string="Street Address")
    street2=fields.Char(string="Street Address 2")
    city=fields.Char(string="City")
    country_id = fields.Many2one('res.country')
    state_id=fields.Many2one('res.country.state','Fed.state')
    zip=fields.Char(string="Zip")
    same_as_communication = fields.Boolean(default=False)
    permanent_address = fields.Char(string="Permanent Address")
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    DOB = fields.Date(string="DOB")
    gender = fields.Selection([('Male','Male'),('Female','Female'),('Other','Other')], string="Gender")
    registration_date = fields.Date(string="Registration Date")
    photo = fields.Image(string="Photo")
    pre_academic_dpt = fields.Selection([('LP', 'LP'), ('UP','UP'),('HS','HS')],string="Previous Academic Department")
    pre_class=fields.Char(string="Previous Class")
    tc=fields.Char(string="TC")
    adhaar_number=fields.Char(string="Aadhaar Number")
    sequence = fields.Char(string='Sequence', copy=False, default="New", readonly=True)

    status=fields.Selection([('Draft','Draft'),('Registration','Registration')])

    @api.model_create_multi
    def create(self, vals):
        """ddddd"""
        for i in vals:
            code = self.env['ir.sequence'].next_by_code('sequence_code')
            i['sequence'] = code
        res = super().create(vals)
        return res