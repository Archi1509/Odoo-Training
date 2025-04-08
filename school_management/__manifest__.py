# -*- coding: utf-8 -*-
{
    'name':'School',
    'version':'0.1',
    'author':'Archi',
    'summery':'School Management ',
    'description':"""
School MAnagement System
========================
    """,
    'sequence':2,
    'category':'academy',
    'depends':['base'],
    'data':[
            'security/ir.model.access.csv',
            'views/school_view.xml'],
    'installable':True,
    'application':True,
    'license':'OEEL-1'

}