# Copyright 2023 Tecnativa - Ernesto García
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_cxml_punchout_order(self):
        cxml_str = ""
        View = self.env["ir.ui.view"].sudo()
        cxml_str = View.render_template(
            "website_sale_punchout.punchout_order_message_xml",
            {"supplier_domain": "DUNS", "supplier_id": "", "order": self},
        )
        return cxml_str
