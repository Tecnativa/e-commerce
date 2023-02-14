# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    # TODO: Maybe this should go in another module
    unspsc = fields.Char()
    # TODO: Implement in compute
    punchout_url = fields.Char()
    # TODO: Not fully implemented. Only product level supported
    punchout_detail_level = fields.Selection(
        selection=[
            ("product", "product"),
            ("store", "store"),
            ("aisle", "aisle"),
            ("shelf", "shelf"),
        ],
        default="product",
    )
