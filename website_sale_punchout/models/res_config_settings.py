# Copyright 2020 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    ariba_unique_name = fields.Char(string="Unique Name", related="company_id.ariba_unique_name", readonly=False)
    ariba_email = fields.Char(string="User Email", related="company_id.ariba_email", readonly=False)
    ariba_supplier_id = fields.Char(string="Supplier ID", related="company_id.ariba_supplier_id", readonly=False)
    ariba_password = fields.Char(string="Password", related="company_id.ariba_password", readonly=False)
