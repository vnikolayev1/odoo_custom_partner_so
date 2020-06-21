import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    express_shipping = fields.Boolean()
