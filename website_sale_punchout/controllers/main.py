# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import datetime

from odoo import fields
from odoo.http import request, route

from odoo.addons.website.controllers.main import Website

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)


class Punchout(Website):
    @route(
        "/punchout_catalog_index.xml",
        type="http",
        auth="public",
        website=True,
        multilang=False,
        sitemap=False,
    )
    def punchout_catalog_index(self, **kwargs):
        current_website = request.website
        Attachment = request.env["ir.attachment"].sudo()
        View = request.env["ir.ui.view"].sudo()
        mimetype = "application/xml;charset=utf-8"
        content = None

        def create_punchout_catalog(url, content):
            return Attachment.create(
                {
                    "datas": base64.b64encode(content),
                    "mimetype": mimetype,
                    "type": "binary",
                    "name": url,
                    "url": url,
                }
            )

        domain = [
            ("url", "=", f"/punchot_catalog-{current_website.id}.xml"),
            ("type", "=", "binary"),
        ]
        catalog = Attachment.search(domain, limit=1)
        if catalog:
            # Check if stored version is still valid
            create_date = fields.Datetime.from_string(catalog.create_date)
            delta = datetime.datetime.now() - create_date
            if delta < SITEMAP_CACHE_TIME:
                content = base64.b64decode(catalog.datas)

        if not content:
            # Remove all catalogs in ir.attachments as we're going to regenerated them
            domain = [
                ("type", "=", "binary"),
                "|",
                ("url", "=like", f"/punchot_catalog-{current_website.id}-%.xml"),
                ("url", "=", f"/punchot_catalog-{current_website.id}.xml"),
            ]
            catalogs = Attachment.search(domain)
            catalogs.unlink()
            products_domain = []
            products = request.env["product.product"].search(products_domain)
            content = View.render_template(
                "website_sale_punchout.punchout_index_catalog_xml",
                {
                    "supplier_domain": "DUNS",
                    "supplier_id": 12346,  # TODO: variable data
                    "products": products,
                    "langs": current_website.language_ids.mapped("code"),
                },
            )
            create_punchout_catalog(
                f"/punchot_catalog-{current_website.id}.xml", content
            )
        return request.make_response(content, [("Content-Type", mimetype)])
