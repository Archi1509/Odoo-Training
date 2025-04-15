{
    'name':'RMA',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'RMA System',
    'description':'RMA System',
    'category':'Management',
    'depends':['base','sale'],
    'data':[
        'security/ir.model.access.csv',

        'wizard/rma_wizard_view.xml',
        'views/sale_rma_view.xml',
        'views/sale_rma_line_view.xml',
        'views/team_view.xml',
        'wizard/rma_line_wizard.xml'
    ],
    'installable': True,
    'license': 'OEEL-1'
}