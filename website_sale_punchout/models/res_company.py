# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    ariba_unique_name = fields.Char(string="Unique Name")
    ariba_email = fields.Char(string="User Email")
    ariba_supplier_id = fields.Char(string="Supplier ID")
    ariba_password = fields.Char(string="Password")
