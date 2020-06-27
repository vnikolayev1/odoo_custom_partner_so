import logging
from odoo.addons.sale_stock.models.sale_order import SaleOrderLine as\
    OriginalSaleOrderLine
from odoo.tools import float_compare
from odoo import fields, models

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    express_shipping = fields.Boolean()

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Launch procurement group run method with required/custom fields
        genrated by a sale order line. procurement group will launch
        '_run_pull', '_run_buy' or '_run_manufacture depending on the
        sale order line product rule.
        """
        precision = self.env['decimal.precision'].precision_get(
            'Product Unit of Measure')
        procurements = []
        express_lines_amnt = 0
        for line in self:
            if line.express_shipping:
                express_lines_amnt += 1
        for line in self:
            if line.state != 'sale' or line.product_id.type not in (
                    'consu', 'product'):
                continue
            qty = line._get_qty_procurement(previous_product_uom_qty)
            if float_compare(qty, line.product_uom_qty,
                             precision_digits=precision) >= 0:
                continue

            group_id = self.env['procurement.group'].create(
                line._prepare_procurement_group_vals())
            line.order_id.procurement_group_id = group_id
            values = line._prepare_procurement_values(group_id=group_id)
            product_qty = line.product_uom_qty - qty

            line_uom = line.product_uom
            quant_uom = line.product_id.uom_id
            product_qty, procurement_uom = line_uom._adjust_uom_quantities(
                product_qty, quant_uom)
            if express_lines_amnt >= 2:
                if line.express_shipping:
                    procurements.append(
                        self.env['procurement.group'].Procurement(
                            line.product_id, product_qty, procurement_uom,
                            line.order_id.partner_shipping_id
                            .property_stock_customer,
                            line.name, line.order_id.name,
                            line.order_id.company_id, values))
        if procurements:
            self.env['procurement.group'].run(procurements)
        return True

    OriginalSaleOrderLine._action_launch_stock_rule = _action_launch_stock_rule
