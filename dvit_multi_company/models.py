# -*- coding: utf-8 -*-

from odoo import models, fields

class MailThread(models.AbstractModel):
    _inherit=['multi.company.abstract','mail.thread']
    _name='mail.thread'

class HrPayrollStructure(models.Model):
    _inherit=['multi.company.abstract','hr.payroll.structure']
    _name='hr.payroll.structure'
