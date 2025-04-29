{
    'name':'Custom Sale',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'Sale System',
    'description':'Sale System',
    'category':'Management',
    'depends':['base','sale','mail','product','purchase'],
    'data':['security/ir.model.access.csv',
            'views/res_config_setting_view.xml',
            'data/mail_template.xml',
            'data/ir_cron.xml',
            'views/purchase_order_view.xml',
            # 'views/purchase_order_line.xml',
    ],
    'installable': True,
    'license': 'OEEL-1'
}