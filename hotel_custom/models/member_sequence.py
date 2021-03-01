from odoo import api, fields, models
from datetime import datetime
from dateutil import relativedelta

class member_sequence_order(models.Model):
    _inherit = 'res.partner'

    temp_field = fields.Many2one('res.partner', string="temp")

    aadhar_card = fields.Char(string="Aadhar Card no.")

    member_seq = fields.Char(string="Service Number", readonly=True, required=True, copy=False, default='New')

    dob = fields.Date(string="Date of Birth")

    age = fields.Integer(string="Age", compute='_onchange_dob')

    gender = fields.Selection(selection=[('m', 'Male'), ('f', 'Female'), ('o', 'Others'), ], string='Gender', default='')

    passport = fields.Char(string="Passport No.")

    # family_details = fields.One2many('member.family.details', 'temp_field', string="Family Details")
    family_details = fields.One2many('res.partner', 'temp_field', string="Family Details")

    relation = fields.Selection(selection=[('s', 'Spouse'), ('c', 'Child'), ], string='Relation', default='')

    nominee = fields.Boolean(string="Nominee")

    # masseur = fields.Boolean(string="Masseur")

    non_member = fields.Boolean(string='Non-Member')

    blood_g = fields.Selection(selection=[('op', 'O+ve'), ('on', 'O-ve'), ('ap', 'A+ve'), ('an', 'A-ve'), ('bp', 'B+ve'), ('bn', 'B-ve'), ('abp', 'AB+ve'), ('abn', 'AB-ve'), ], string='Blood Group', default='')

    # kan_member_seq = fields.Char(string="HEY")

    @api.model
    def create(self, vals):
        if vals.get('member_seq', 'New') == 'New':
            vals['member_seq'] = self.env['ir.sequence'].next_by_code(
                'self.service') or 'New'
        result = super(member_sequence_order, self).create(vals)
        return result

    @api.onchange('dob')
    def _onchange_dob(self):
        for record in self:
            if record.dob:
                date1 = datetime.strptime(str(record.dob), '%Y-%m-%d')
                date2 = datetime.today()
                r = relativedelta.relativedelta(date2, date1)
                record.age = r.years
            else:
                record.age = 0

class HotelManagement(models.Model):
    _inherit = 'hotel.reservation'

    in_field = fields.Boolean(string="Field", readonly=True, default=True)

    partner_id = fields.Many2one('res.partner', string="New_Guest")

    check_in = fields.Datetime(string="Check-In Date")

    check_out = fields.Datetime(string="Check-Out Date")

    def check_in_button(self):
        for record in self:
            record.check_in = datetime.today()

    def check_out_button(self):
        for record in self:
            record.check_out = datetime.today()

    @api.onchange('in_field')
    def _onchange_in_field(self):
        if self.in_field:
            return {'domain': {'partner_id': ['|',('membership_state', '=', 'paid'),(('membership_state', '=', 'old'))]}}


class MembershipProductManagement(models.Model):
    _inherit = 'product.template'

# class RoomBookingManagement(models.Model):
#     _name = 'something.else'
#
#     _inherit = 'quick.room.reservation'
#
#     new_field = fields.Char(string="New")
#
#     partner_id = fields.Many2one('res.partner', string="Works")
# class member_family_details(models.Model):
#     _name = 'member.family.details'
#
#     temp_field = fields.Many2one('res.partner', string="temp")
#
#     member_name = fields.Char(string="Name")
#
#     relation = fields.Selection(selection=[('s', 'Spouse'), ('c', 'Child'), ], string='Relation', default='')
#
#     age = fields.Integer(string="Age")
#
#     rel_gender = fields.Selection(selection=[('m', 'Male'), ('f', 'Female'), ('o', 'Others'), ], string='Gender', default='')
#
#     nominee = fields.Boolean(string="Nominee")
