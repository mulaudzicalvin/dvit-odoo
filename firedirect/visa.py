from datetime import timedelta, date, datetime

import pytz

from openerp import models, fields, api, _, SUPERUSER_ID, tools
from openerp.exceptions import Warning
from openerp.osv import osv

from dateutil import parser

import logging
_logger = logging.getLogger(__name__)

    
class firedirect_expiring_visa(models.TransientModel):
    _name='firedirect.expiringvisa1'

    @api.model
    def checkExpiringVisa(self):
        _logger.error("checkExpiringVisa checkExpiringVisa")

        date30=(datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        daten20=(datetime.now() - timedelta(days=20)).strftime("%Y-%m-%d")
        
        ids=self.env['hr.employee'].search([('visa_expiry','<=',date30),('visa_expiry_sent','<',daten20)])#
        
        #TEMPLATE
        _logger.error("10 D LIST %r",ids)
        for id in ids:
            _logger.error("10 D ITEM %r",id)
            template = self.env.ref('firedirect.email_template_visa_expiry', False)
            if template:
                mail_message = template.send_mail(id.id)
                id.visa_expiry_sent = datetime.now()
        return True
