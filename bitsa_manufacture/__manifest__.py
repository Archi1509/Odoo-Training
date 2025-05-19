{
    'name':'Bista Manufacture',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'Bista Manufacture',
    'description':'Bista Manufacture',
    'category':'Management',
    'depends':['base','sale','sale_stock'],
    'data':[
        'security/ir.model.access.csv',
        'views/product_product_view.xml',
        'views/mrp_production.xml',
        'views/sale_order_view.xml',
        # 'views/stock_picking_view.xml',
        'wizard/add_serial_view.xml',
        'wizard/manufacture_report_view.xml',
        'wizard/update_product_serial_view.xml',
        'wizard/replace_product_read_file_view.xml',
    ],
    'installable': True,
    'license': 'OEEL-1'
}