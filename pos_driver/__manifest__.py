{
    'name' : 'Point Of Sale Delivery',
    'summary': 'Point Of Sale Delivery',
    'description':
        """
Point Of Sale Driver
=====================
    adds a button in "point of sales ui" to select a delivery driver 
        """,
    'version': '10.0.4.0',
    'category': 'Point of Sale',
    'author': 'DVIT.me',
    'website': 'http://dvit.me',
    'license': 'AGPL-3',
    'depends' : ['point_of_sale', 'hr'],
    'data': ['static/src/xml/data.xml'],
    'qweb': ['static/src/xml/qweb.xml'],
    'installable': False,
    'auto_install': False,
    'application': False,

}
