{
    'name':'practical archi',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'2nd Evaluation Test',
    'description':'2nd Evaluation Test',
    'category':'Management',
    'depends':['base','sale','product','account','mail','purchase','sale_stock'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/pharmacy_records.xml',
        'data/purchase_order_email.xml',
        'views/sale_pharmacy_view.xml',
        'views/product_product_view.xml',
        'views/account_move_view_inherit.xml',
        'views/sale_order_inherit.xml',
        'views/mail_activity_schedule_view_inherit.xml',
        'views/delivery_slip_inherit.xml',
        'views/res_config_settings.xml',
        'wizard/custom_wizard_view.xml',
        'views/stock_picking_view_inherit.xml',

    ],
    'installable': True,
    'license': 'OEEL-1'
}