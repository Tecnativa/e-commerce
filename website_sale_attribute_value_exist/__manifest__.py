# Copyright 2019 Tecnativa - Victor M.M. Torres
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Website Sale Attribute Value Exist',
    'summary': 'Allow hide attributes values not used in variants',
    'version': '11.0.1.0.0',
    'development_status': 'Beta',
    'category': 'Website',
    'website': 'https://github.com/OCA/e-commerce',
    'author': 'Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'website_sale',
    ],
    'data': [
        'views/templates.xml',
    ],
}
