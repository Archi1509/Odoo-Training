{
    'name':'CRM',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'CRM System',
    'description':'CRM System',
    'category':'Management',
    'depends':['base','crm','sale_crm','sale'],
    'data':[
        'security/ir.model.access.csv',
        'views/crm_lead_view.xml',
        'views/stage_percentage_view.xml',
        'views/sale_order_view.xml',
    ],
    'installable': True,
    'license': 'OEEL-1'
}