# -*- coding: utf-8 -*-
{
    'name':'BookStore',
    'version':'0.1',
    'author':'Archi',
    'summery':'BookStore Management',
    'description':"""
    School MAnagement System
    ========================
        """,
    'sequence':4,
    'category':'Management',
    'depends':['base'],
    'data':[
            'security/ir.model.access.csv',
            'views/bookstore_view.xml',
            'views/author_model_view.xml',
            'views/customer_view.xml',
            'views/genres_view.xml',
            'views/order_view.xml',
            'views/orderline_view.xml',
            'views/publisher_view.xml',
            'wizard/book_wizard_view.xml'
        ],
    'installable':True,
    'application':True,
    'license':'OEEL-1'

}