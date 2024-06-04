{
    'name': "Web Customer Portal",
    'summary': "Allow Customers to get access to portal for their details",
    'description': """
    Customers Web Portal.
    """,
    'author': "Faizan Lodhi",
    'website': "http://www.example.com",
    'category': 'web portal',
    'version': '14.0.1',
    'sequence': -1,
    'depends': ['base','contacts','sale', 'website','account', 'stock', "project"],
    'data': [
        'security/security_rules.xml',
        'views/res.partner_ext.xml',
        'views/static_templates.xml',
        'views/template_qweb_view.xml',

    ],


    "qweb": [],
    'installable': True,
    'application': True,
    'auto_install': True,
}

