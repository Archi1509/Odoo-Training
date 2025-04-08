{
    'name':'LMS',
    'author':'Archi',
    'version':'0.1',
    'sequence':'-10',
    'summery':'Library Management System',
    'description':'Library System',
    'category':'Management',
    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',
        'views/book_view.xml',
        'views/author_view.xml',
        'views/category_view.xml'
    ],
    'installable': True,
    'license': 'OEEL-1'
}