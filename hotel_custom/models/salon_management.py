from odoo import api, fields, models
from datetime import datetime
from dateutil import relativedelta

class BookingInformation(models.Model):
    _inherit = 'salon.booking'

    source = fields.Selection(selection=[('w', 'Walk-In'), ('m', 'Member'), ('g', 'Guest'), ], string='Source', default='')

    member_name = fields.Many2one('res.partner', string="Name")

    guest_name = fields.Many2one('res.partner', string="Name", no_create=False)

    name = fields.Char(compute="_onchange_source")

    membership_id = fields.Char(string='Membership ID', compute="_onchange_member_name", readonly=True)

    n_gender = fields.Selection(selection=[('m', 'Male'), ('f', 'Female'), ('o', 'Others'), ], string='Gender', default='')

    pref_gender = fields.Selection(selection=[('m', 'Male'), ('f', 'Female'), ('o', 'Others'), ], string='Preferred Gender', default='')

    # contact = fields.Char(string="Mobile No.")

    nationality = fields.Many2one('res.country', string="Nationality")

    # pref_date = fields.Date(string="Preferred date", required=True)

    # service_type = fields.Many2one('salon.service', string="Service Type")

    email = fields.Char(string="Email")

    remark = fields.Char(string="Remarks/ Extra Instructions")

    masseur_info = fields.Many2one('masseur.management', string="Masseur")

    # chair_id = fields.Many2one('salon.chair', string="Chair", compute="_onchange_p_gender", readonly=False)

    @api.depends('member_name')
    def _onchange_member_name(self):
        for record in self:
            if record.member_name:
                record.membership_id = record.member_name.member_seq
                record.n_gender = record.member_name.gender
                record.phone = record.member_name.phone
                record.nationality = record.member_name.country_id
                record.email = record.member_name.email
            else:
                record.membership_id = ""
                record.n_gender = ""
                record.phone = False
                record.nationality = False
                record.email = ""



    @api.onchange('source')
    def _onchange_source(self):
        for record in self:
            if record.source != 'm':
                record.name = record.guest_name.name
            elif record.source == 'm':
                record.name = record.member_name.name
            else:
                record.name = 'none'

    # @api.onchange('chair_id')
    # def _onchange_chair(self):
    #     for record in self:
    #         if record.chair_id:
    #             record.masseur_info = record.chair_id.user_of_chair.name
    #         else:
    #             record.masseur_info = ""

    @api.onchange('pref_gender')
    def _onchange_p_gender(self):
        for record in self:
            if record.pref_gender == 'm':
                return {'domain': {'masseur_info': [('gender', '=', 'm')]}}
            elif record.pref_gender == 'f':
                return {'domain': {'masseur_info': [('gender', '!=', 'm')]}}
            else:
                return {'domain': {}}

    # @api.onchange('source')
    # def _onchange_source_custom(self):
    #     for record in self:
    #         if record.source == 'm':
    #             return {'domain': {'member_name': ['|', ('membership_state', '=', 'free'), ('membership_state', '=', 'paid')]}}
            # elif record.source == 'g':
            #     return {'attribute': {'member_name': [('non_member', '=', True)]}}
            # elif record.source == 'm':
            #     return {'attribute': {'member_name': [('non_member', '!=', True)]}}


# class ChairManagement(models.Model):
#     _inherit = 'res.users'
#
#     masseur = fields.Boolean(string="Masseurs")
#
#     c_gender = fields.Selection(selection=[('Male', 'Male'), ('Female', 'Female'),], string='Gender', default='')

class HotelBookingManagement(models.TransientModel):
    # _name = 'custom.change.wizard'

    _inherit = 'quick.room.reservation'

    gender = fields.Boolean(string='gender', default=True)

    @api.onchange('gender')
    def _onchange_gender(self):
        if self.gender:
            return {'domain': {'partner_id': ['|',('membership_state', '=', 'paid'),('membership_state', '=', 'old')]}}

class MasseurManagement(models.Model):
    _name = 'masseur.management'

    name = fields.Char(string="Name")

    gender = fields.Selection(selection=[('m', 'Male'), ('f', 'Female'), ], string='Gender', default='')






