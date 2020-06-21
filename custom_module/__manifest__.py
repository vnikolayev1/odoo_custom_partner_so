{
    'name': 'Custom module',

    'summary': 'Custom module that alters partner and sales order.',

    'author': 'Vnikolayev1',

    'category': 'Other Category',
    'license': 'OPL-1',
    'version': '13.0.0.0.0',
    'depends': [
        'base',
        'contacts',
        'sale_management',
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/partner_view.xml',
        'views/sale_order.xml',
    ],
    'installable': True,
    'application': False,

}
