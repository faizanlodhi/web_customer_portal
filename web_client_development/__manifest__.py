{
    'name': "Web Client Development",
    'summary': "Allow Customers to get access to portal for their details",
    'description': """
    Customers Web Portal.
    """,
    'author': "Faizan Lodhi",
    'website': "http://www.example.com",
    'category': 'web portal',
    'version': '14.0.1',
    'sequence': -1,
    'depends': ['base','contacts','sale', 'web','website','account', 'stock', "project"],
    'data': [
        'views/templates.xml',
        'views/res.partner_ext.xml',
        'views/q_web_template.xml',
    ],


    # "qweb": [
    #     '/static/src/xml/q_web_template.xml'
    # ],
    'installable': True,
    'application': True,
    'auto_install': True,
}

