# See LICENSE file for full copyright and licensing details.

{
    "name": "Hotel Reservation Inherit",
    "version": "13.0.1.0.0",
    "author": "Odoo Community Association (OCA), Serpent Consulting \
                Services Pvt. Ltd., Odoo S.A.",
    "category": "Generic Modules/Hotel Reservation",
    "license": "AGPL-3",
    "summary": "Manages Guest Reservation & displays Reservation Summary",
    "website": "https://github.com/OCA/vertical-hotel/",
    "depends": ["hotel_reservation", "account"],
    "data": [
        "view/account_move_view_inherit.xml",


    ],
    "demo": [],
    "qweb": [],
    "external_dependencies": {"python": ["dateutil"]},
    "installable": True,
}
