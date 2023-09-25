# Copyright 2023 Tecnativa - David Vidal
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import base64
import datetime
import logging
from uuid import uuid4

import werkzeug
from lxml import etree

from odoo import fields
from odoo.http import request, route

from odoo.addons.payment.controllers.portal import PaymentProcessing
from odoo.addons.website.controllers.main import Website

SITEMAP_CACHE_TIME = datetime.timedelta(hours=12)
_logger = logging.getLogger(__name__)


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
        company_id = request.website.company_id

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
                    "supplier_id": company_id.ariba_unique_name,
                    "products": products,
                    "langs": current_website.language_ids.mapped("code"),
                },
            )
            create_punchout_catalog(
                f"/punchot_catalog-{current_website.id}.xml", content
            )
        return request.make_response(content, [("Content-Type", mimetype)])

    @route(
        "/ProfileRequest.xml",
        type="http",
        auth="public",
        website=True,
        multilang=False,
        sitemap=False,
        csrf=False,
    )
    def profile_request_punchout(self, **kwargs):
        View = request.env["ir.ui.view"].sudo()
        user = request.env["res.users"].sudo().browse(request.uid)
        company_id = user.company_id
        mimetype = "application/xml;charset=utf-8"
        content = View.render_template(
            "website_sale_punchout.punchout_profile_request_xml",
            {
                "supplier_domain": "DUNS",
                "ariba_email": company_id.ariba_email,
                "supplier_id": company_id.ariba_unique_name,
                "ariba_password": company_id.ariba_password,
            },
        )
        return request.make_response(content, [("Content-Type", mimetype)])

    @route(
        "/punchoutsetuprequest.xml",
        type="http",
        auth="public",
        methods=["POST", "GET"],
        sitemap=False,
        csrf=False,
    )
    def punch_setup_request(self, **kwargs):
        # Guardar SID con datos de inicio de sesión
        sid = ""
        w_request = request.httprequest.environ.get("werkzeug.request")
        cxml_request_data = w_request.data
        cxml_tree = etree.XML(cxml_request_data)
        cxml_tree.xpath("//Header/Sender/Credential")[0]
        identity = cxml_tree.xpath("//Header/Sender/Credential/Identity")[0].text
        shared_secret = cxml_tree.xpath("//Header/Sender/Credential/SharedSecret")[
            0
        ].text
        if request.env["session.punchout"].validate_puchout_credential(
            identity, shared_secret
        ):
            sid = uuid4().hex
            request.env["session.punchout"].sudo().create(
                {"sid": sid, "identity": identity, "shared_secret": shared_secret}
            )
        else:
            _logger.info("ERRORES AQUI")
            # TODO: Retornar respuesta con error correspondiente
        # TODO: obtener información de inicio de sesión
        View = request.env["ir.ui.view"].sudo()
        user = request.env["res.users"].sudo().browse(request.uid)
        base_url = request.env["ir.config_parameter"].sudo().get_param("web.base.url")
        company_id = user.company_id
        mimetype = "application/xml;charset=utf-8"
        content = View.render_template(
            "website_sale_punchout.punchout_setup_request_xml",
            {
                "supplier_domain": "DUNS",
                "ariba_email": company_id.ariba_email,
                "supplier_id": company_id.ariba_unique_name,
                "ariba_password": company_id.ariba_password,
                "BuyerCookie": "",
                "start_url": base_url + "/puchout_redirect_shop" + "?sid=" + sid,
            },
        )
        return request.make_response(content, [("Content-Type", mimetype)])

    @route(
        "/puchout_redirect_shop",
        type="http",
        auth="public",
        methods=["GET"],
        csrf=False,
    )
    def punch_setup_request_shop(self, sid, **kwargs):
        # TODO: tomar datos de inicio de sesión de SID
        if sid:
            spunchout_id = (
                request.env["session.punchout"].sudo().search([("sid", "=", sid)])
            )

            request.session.authenticate(
                request.db, spunchout_id.identity, spunchout_id.shared_secret
            )
        url = "/shop"
        return werkzeug.utils.redirect(url)

    @route(
        "/shop/payment/validate_punchout",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
        # Hacer el CXML del punchoutorderMessage ver como retornar la url de carrito del buyer

        order = False
        if sale_order_id is None:
            order = request.website.sale_get_order()
        else:
            order = request.env["sale.order"].sudo().browse(sale_order_id)
            assert order.id == request.session.get("sale_last_order_id")

        if transaction_id:
            tx = request.env["payment.transaction"].sudo().browse(transaction_id)
            assert tx in order.transaction_ids()
        elif order:
            tx = order.get_portal_last_transaction()
        else:
            tx = None
        if not order or (order.amount_total and not tx):
            return request.redirect("/shop")

        if order and not order.amount_total and not tx:
            order.with_context(send_email=True).action_confirm()
            return request.redirect(order.get_portal_url())

        # clean context and session, then redirect to the confirmation page
        request.website.sale_reset()
        if tx and tx.state == "draft":
            return request.redirect("/shop")

        PaymentProcessing.remove_payment_transaction(tx)
        return request.redirect("/shop/confirmation")
