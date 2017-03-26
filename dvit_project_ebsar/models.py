# -*- coding: utf-8 -*-

from openerp import models, fields, api

class project_project(models.Model):
    _inherit = 'project.project'

    order_number = fields.Char(string="رقم الطلب" )
    date_assigned = fields.Date(string="تاريخ الاسناد")
    client_name = fields.Char(string="اسم المشترك")
    client_mobile = fields.Char(string="جوال المشترك")
    es_number = fields.Char(string="رقم محطة كهرباء المشترك")
    meter_numbers = fields.Integer(string="العدادات المعتمدة")
    in_number = fields.Char(string="الرقم الداخلي للمشروع")


class ProjectTask(models.Model):
    _inherit = 'project.task'

    billable = fields.Boolean(string="مستخلص")
    licensable = fields.Boolean(string="رخصة")
    date_valuated = fields.Date(string="تاريخ استلام وتقييم مبلغ تكلفة العمل في التقرير" )
    date_budget_start = fields.Date(string="تاريخ بداية موازنة المو اد والاعمال" )
    date_budget_end = fields.Date(string="تاريخ نهاية موازنة المواد والاعمال" )
    date_certificate = fields.Date(string="تاريخ شهادة الإنجاز" )
    date_sent = fields.Date(string="تاريخ إرسال المعامله" )
    date_invoiced = fields.Date(string="تاريخ فاتورة رقم المستخلص للتوقيع" )
