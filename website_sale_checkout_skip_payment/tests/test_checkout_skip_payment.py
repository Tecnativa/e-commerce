# Copyright 2018 Tecnativa - Sergio Teruel
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests.common import HttpCase


class WebsiteSaleHttpCase(HttpCase):

    def setUp(self):
        super().setUp()
        # Active skip payment for Mitchel Admin
        self.partner = self.env.ref('base.partner_admin')
        self.partner.write({
            'customer': True,
            'skip_website_checkout_payment': True,
        })
        # Use a high website_sequence to force display it on first shop page.
        # I use a service product to avoid to the delivery provider extra step.
        self.product_template = self.env['product.template'].create({
            'name': 'Product test skip payment',
            'type': 'service',
            'list_price': 750.00,
            'website_published': True,
            'website_sequence': 9999,
        })

    def test_ui_website(self):
        """Test frontend tour."""
        tour = (
            "odoo.__DEBUG__.services['web_tour.tour']",
            "website_sale_checkout_skip_payment",
        )
        self.browser_js(
            url_path="/shop",
            code="%s.run('%s')" % tour,
            ready="%s.tours['%s'].ready" % tour,
            login="admin",
        )
