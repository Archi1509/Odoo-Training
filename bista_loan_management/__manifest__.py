{
    'name':'Bista Loan Management',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'Loan Management System',
    'description':'Loan Management System',
    'category':'Management',
    'depends':['base','account','product'],
    'data':[
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/emi_product.xml',
        'data/ir_cron.xml',
        'data/mail_template.xml',
        'views/loan_view.xml',
        'views/interest_rate.xml',
        'views/acount_move_view.xml',
        'views/approval_team_view.xml',
    ],
    'installable': True,
    'license': 'OEEL-1'
}