# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Punchot Catalog",
    "summary": "Allows to generate a Punchout Catalog to upload to Ariba NetWork"
    " categories",
    "version": "15.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/OCA/e-commerce",
    "maintainers": ["chienandalu"],
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["website_sale", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/punchout_index_catalog_templates.xml",
        "views/res_config_settings_view.xml",
        "views/website_shop.xml",
    ],
}
