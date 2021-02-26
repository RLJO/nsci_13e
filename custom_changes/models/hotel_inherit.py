from datetime import timedelta

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HotelReservationInherit(models.Model):

    _inherit = "hotel.reservation"

    def create_folio(self):
        """
        This method is for create new hotel folio.
        -----------------------------------------
        @param self: The object pointer
        @return: new record set for hotel folio.
        """
        hotel_folio_obj = self.env["hotel.folio"]
        for reservation in self:
            folio_lines = []
            checkin_date = reservation["checkin"]
            checkout_date = reservation["checkout"]
            duration_vals = self._onchange_check_dates(
                checkin_date=checkin_date,
                checkout_date=checkout_date,
                duration=False,
            )
            duration = duration_vals.get("duration") or 0.0
            folio_vals = {
                "date_order": reservation.date_order,
                "warehouse_id": reservation.warehouse_id.id,
                "partner_id": reservation.partner_id.id,
                "pricelist_id": reservation.pricelist_id.id,
                "partner_invoice_id": reservation.partner_invoice_id.id,
                "partner_shipping_id": reservation.partner_shipping_id.id,
                "checkin_date": reservation.checkin,
                "checkout_date": reservation.checkout,
                "duration": duration,
                "reservation_id": reservation.id,
            }
            for line in reservation.reservation_line_ids:
                for r in line.reserve:
                    folio_lines.append(
                        (
                            0,
                            0,
                            {
                                "checkin_date": checkin_date,
                                "checkout_date": checkout_date,
                                "product_id": r.product_id and r.product_id.id,
                                "name": reservation["reservation_no"],
                                "price_unit": r.list_price,
                                "product_uom_qty": duration,
                                "is_reserved": True,
                            },
                        )
                    )
                    r.write({"status": "occupied", "isroom": False})
            folio_vals.update({"room_line_ids": folio_lines})
            folio = hotel_folio_obj.create(folio_vals)
            for rm_line in folio.room_line_ids:
                rm_line.product_id_change()
            # self.write({"folios_ids": [(6, 0, folio.ids)], "state": "done"})
            self.write({"folios_ids": [(6, 0, folio.ids)]})
        # return True

        return {'view_mode': 'form',
                'res_id': folio.id,
                'type': 'ir.actions.act_window',
                'res_model': 'hotel.folio',
                'target': 'current'
                }



class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"


    def post(self):
        res = super(AccountPaymentInherit, self).post()

        inv_id = self.env['account.move'].browse(self._context.get('active_id'))

        # hotel_brw = self.env['hotel.reservation'].search({'id', '=', inv_id.folio_id.id})
        # hotel_brw.confirm_reservation()
        inv_id.folio_id.reservation_id.confirm_reservation()

        return res


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    folio_id = fields.Many2one('hotel.folio', 'Folio')