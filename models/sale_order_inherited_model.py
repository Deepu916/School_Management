"""Sale Order Inherited Model"""
# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrder(models.Model):
    """Sale Order Inherited Model"""
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('admitted', 'Admitted'),('sale','Sale Order')],
                             ondelete={'admitted': 'set default'})
