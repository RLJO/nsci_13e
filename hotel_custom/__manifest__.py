# See LICENSE file for full copyright and licensing details.

{
    "name": "Hotel Reservation Management",
    "version": "13.0.1.0.0",
    "author": "Odoo Community Association (OCA), Serpent Consulting \
                Services Pvt. Ltd., Odoo S.A.",
    "category": "Generic Modules/Hotel Reservation",
    "license": "AGPL-3",
    "summary": "Manages Guest Reservation & displays Reservation Summary",
    "website": "https://github.com/OCA/vertical-hotel/",
    "depends": ["hotel", "stock", "mail", "base", "membership", "hotel_reservation"],
    "data": [
        "security/ir.model.access.csv",
        "views/member_sequence.xml",
        "views/salon_management.xml",
        "data/sequence.xml",
    ],
    "demo": [],
    "installable": True,
}
