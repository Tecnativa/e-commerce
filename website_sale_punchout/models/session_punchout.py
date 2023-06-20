# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class SessionPunchout(models.Model):
    _name = "session.punchout"
    _description = "Punchout Session"

    sid = fields.Char("SID", readonly=True)
    shared_secret = fields.Char()
    identity = fields.Char()

    def validate_puchout_credential(self, identity, shared_secret):
        # TODO: como validare estos datos?
        return True
