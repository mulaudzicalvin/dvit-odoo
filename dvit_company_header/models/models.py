# -*- coding: utf-8 -*-

from odoo import models, fields, api

class resCompany(models.Model):
    _inherit = 'res.company'



    header = fields.Binary("Header")
    footer = fields.Binary("Footer")

