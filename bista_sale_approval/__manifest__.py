{
    'name':'Sale Approval',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'Sale Approval System',
    'description':'Sale Approval System',
    'category':'Management',
    'depends':['base','sale'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',

    ],
    'installable': True,
    'license': 'OEEL-1'
}