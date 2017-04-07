# -*- coding: utf-8 -*-

from datetime import timedelta, date, datetime

import pytz

from openerp import models, fields, api, _, SUPERUSER_ID, tools
from openerp.exceptions import Warning
from openerp.report import report_sxw 
from lxml import etree
from openerp.osv import osv

from dateutil import parser


from collections import defaultdict

import logging
_logger = logging.getLogger(__name__)


reservationmailsent = 0

class view(osv.osv):
    _inherit = ['ir.ui.view']

    def __init__(self, pool, cr):
        super(view, self).__init__(pool, cr)
        super(view, self)._columns['type'].selection.append(('instcalendar','InstCalendar'))

class firedirect_area(models.Model):
    _name = 'firedirect.area'
    _description = 'Firedirect Area'
    _rec_name = 'address'

    country_id = fields.Many2one('res.country', string='Country', required=True)
    city = fields.Char(string='City', required=True)
    address = fields.Char(string='Address', required=True)

class firedirect_room(models.Model):
    _name = 'firedirect.room'
    _description = 'Firedirect Room'

    name = fields.Char(string='Room Name', required=True)
    number = fields.Char(string='Room #', required=True)
    capacity = fields.Integer(string='Room Capacity', required=True)
    area_id = fields.Many2one('firedirect.area', string='Area', required=True)
    course_ids = fields.Many2many('firedirect.course', string='Course', required=True)
    reservations = fields.One2many('firedirect.reservation','room_id')
    day_reservations = fields.Many2many('firedirect.reservation',compute='_reservations',store=False)
    is_free = fields.Boolean(compute='_is_free')
    
    at = fields.Date(string = 'Day')
    
    course_names = fields.Char(compute='_cnames')
    instructor_names = fields.Char(compute='_inames')
    reserved = fields.Char(compute='_res')
    available = fields.Char(compute='_av')
    
    @api.one
    @api.depends('day_reservations','at')
    def _cnames(self):
        for record in self:
            cns=[]
            for rese in record.day_reservations:
                cns.append(rese.course_id.name)
            record.course_names=', '.join(cns)  

    @api.one
    @api.depends('day_reservations','at')
    def _inames(self):
        for record in self:
            ins=[]
            for rese in record.day_reservations:
                ins.append(rese.instructor_id.name)
            record.instructor_names=', '.join(ins)

    @api.one
    @api.depends('day_reservations','at')
    def _res(self):
        for record in self:
            reser=[]
            for rese in record.day_reservations:
                reser.append(str(len(rese.student_ids)))
            record.reserved=', '.join(reser)
            
    @api.one
    @api.depends('day_reservations','at')
    def _av(self):
        for record in self:
            ava=[]
            for rese in record.day_reservations:
                ava.append(str(record.capacity-len(rese.student_ids)))
            record.available=', '.join(ava)


    @api.one
    @api.depends('reservations','at')
    def _reservations(self):
        for record in self:
            if record.at:
                record.day_reservations=record.reservations.search([('start_date','<=',record.at),('end_date','>=',record.at),('room_id','=',record.id)])
            else:
                record.day_reservations=record.reservations.search([('id','=',0)])

    @api.one
    @api.depends('day_reservations')
    def _is_free(self):
        for record in self:#WRONG??
            record.is_free=len(record.reservations.search([('start_date','<=',datetime.datetime.now().strftime("%Y-%m-%d")),('end_date','>=',datetime.datetime.now().strftime("%Y-%m-%d"))]))==0

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        search2=[]
        for sterm in args:
            if sterm[0] != 'at':
                search2.append(sterm)
        res = super(firedirect_room, self).search(search2, offset=offset, limit=limit, order=order, count=count)
        found = False
        for sterm in args:
            if sterm[0] == 'at':
                for obj in res:
                    obj.at = sterm[2]
                found=True
                break
        if not found:
            for obj in res:
                obj.at=False
        return res

    
class firedirect_course(models.Model):
    _name = 'firedirect.course'
    _description = 'Firedirect Course'

    name = fields.Char(string='Course Name', required=True)
    duration = fields.Integer(string='Duration (in days)', required=True)
    instructor_id = fields.Many2many('hr.employee','instructor_course_rel','course_id','employee_id', string='Instructor', required=True, domain=[('job_id','=','Instructor')])
    Reservations = fields.One2many('firedirect.reservation','course_id')


class firedirect_student(models.Model):
    _name = 'firedirect.student'
    _description = 'Firedirect Student'
    
    name = fields.Char(string='Student Name', required=True)
    company_id = fields.Many2one('res.partner', string='Company', required=True, domain=[('customer','=',True),('is_company','=',True)])
    position = fields.Char(string='Position', required=True)
    rig = fields.Char(string='RIG', required=True)
    nationality_id = fields.Many2one('res.country', string='Nationality', required=True)
    email = fields.Char('E-Mail', size=240)
    mobile = fields.Char('Mobile No.', size=240)
    id_type = fields.Selection([('iqama','Iqama'),('passport','Passport'),('saudi_id','Saudi ID'),('staff_id','Staff ID')], 'ID Type')
    id_no = fields.Char('ID No.')
    
class firedirect_reservation(models.Model):
    _name = 'firedirect.reservation'
    _inherit = ['mail.thread']
    _description = 'Firedirect Reservation'

    course_id = fields.Many2one('firedirect.course', string='Course Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    room_id = fields.Many2one('firedirect.room', string='Room', required=True)
    instructor_id = fields.Many2one('hr.employee', string='Instructor', required=True,domain=[('job_id','=','Instructor')])
    student_ids = fields.Many2many('firedirect.student','firedirect_reservation_student','reservtion_id','student_id', string='Students', required=True)
    all_day = fields.Boolean('All Day', default = False)
    start_time = fields.Char(string='Start Time', required=True)
    end_time = fields.Char(string='End Time', required=True)
    rid = fields.Integer(string='RID', required=False,compute='_get_rid')
    
    def create(self, cr, user, vals, context=None):
        res=super(firedirect_reservation, self).create(cr, user, vals, context)
        if res:
            self.sendMail( cr, user, context, res)
        return res
    
    @api.multi
    @api.depends('course_id', 'room_id', 'start_date','end_date', 'start_time','end_time')
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,record.course_id.name + " / "+record.room_id.name+"["+record.start_time+"-"+record.end_time+"]"))
        return result
    
    
    
    @api.one
    def _get_rid(self):
        for obj in self:
            obj.rid=obj.id

    @api.depends('rid')
    @api.onchange('start_date','end_date','start_time','end_time')
    def _onchange_startdate(self):
#        if self.start_time:
#            if self.end_time:
#                if self.start_time>self.end_time:
#                    tmp=self.end_time
#                    self.end_time=self.start_time
#                    self.start_time=tmp
        if self.end_date:
            if self.start_date:
                if self.start_date>self.end_date:
                    tmp=self.end_date
                    self.end_date=self.start_date
                    self.start_date=tmp
                if self.start_time:
                    if self.end_time:
                        #update list of locations and instructors based on busy or not
                        iids=self._get_invalid_instructor_ids()
                        iidsc=self._get_confirmed_holiday_instructor_ids()
                        iidsp=self._get_pending_holiday_instructor_ids()
                        iids = iids + iidsc
                        rids=self._get_invalid_room_ids()
                        value={}
                        if self.instructor_id.id in iids:
                            value['instructor_id'] = False
                            self.instructor_id = False
                        if self.room_id.id in rids:
                            value['room_id'] = False
                            self.room_id = False
                            
                        if self.instructor_id.id in iidsp:
                            return {
                                'warning': {
                                    'title': "Instructor has requested a leave",
                                    'message': "The selected instructor has requested a leave that may conflict with the selected date range, please contact the manager for more information",
                                },
                                'domain': {'room_id': [('id', 'not in', rids),('capacity', '>=', len(self.student_ids))],'instructor_id': [('id', 'not in', iids),('job_id','=','Instructor')]},
                                'value': value
                            }
                            
                        return {
                            'domain': {'room_id': [('id', 'not in', rids),('capacity', '>=', len(self.student_ids))],'instructor_id': [('id', 'not in', iids),('job_id','=','Instructor')]},
                            'value': value
                        }

    @api.depends('rid')
    @api.onchange('student_ids')
    def _onchange_students(self):
        if self.room_id :
            if len(self.student_ids) > self.room_id.capacity :
                self.room_id = False
                return {
                    'warning': {
                        'title': "Too many students",
                        'message': "The selected room doesn't have enough seats for the all the students",##
                    },
                    'domain': {'room_id': [('capacity', '>=', len(self.student_ids))]},
                    'value':{'room_id':False}                  
                }
        if self.end_date:
            if self.start_time:
                if self.start_date:
                    if self.end_time:
                        return self._onchange_startdate()
        return {
            'domain': {'room_id': [('capacity', '>=', len(self.student_ids))]},                    
        }


    def _get_confirmed_holiday_instructor_ids(self):
        self._cr.execute("select distinct employee_id from hr_holidays where ((date_from>='" + self.start_date + "' and date_from<='" + self.end_date + "' ) or (date_from<='" + self.start_date + "' and date_to>='" + self.start_date + "' ) or (date_to>='" + self.start_date + "' and date_to<='" + self.end_date + "' )) and (state='validate1' or state='validate2')")
        ids = map(lambda x : x[0],self._cr.fetchall())
        return ids
        
    def _get_pending_holiday_instructor_ids(self):
        self._cr.execute("select distinct employee_id from hr_holidays where ((date_from>='" + self.start_date + "' and date_from<='" + self.end_date + "' ) or (date_from<='" + self.start_date + "' and date_to>='" + self.start_date + "' ) or (date_to>='" + self.start_date + "' and date_to<='" + self.end_date + "' )) and (state='confirm')")
        ids = map(lambda x : x[0],self._cr.fetchall())
        return ids
        
    def _get_invalid_instructor_ids(self):
        self._cr.execute("select distinct instructor_id from firedirect_reservation where id != " + str(self.rid) + " and ((start_date>='" + self.start_date + "' and start_date<='" + self.end_date + "' ) or (start_date<='" + self.start_date + "' and end_date>='" + self.start_date + "' ) or (end_date>='" + self.start_date + "' and end_date<='" + self.end_date + "' )) and ((('2001-01-01 '||start_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||start_time)::timestamp <= '2001-01-01 " + self.end_time + "' ) or (('2001-01-01 '||end_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||end_time)::timestamp <= '2001-01-01 " + self.end_time + "' ) or (('2001-01-01 '||end_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||start_time)::timestamp <= '2001-01-01 " + self.start_time + "' ))")
        ids=[]
        for record in self._cr.fetchall():
            ids.append(record[0])
        return ids
    
    def _get_invalid_room_ids(self):
        self._cr.execute("select distinct room_id from firedirect_reservation where id != " + str(self.rid) + " and ((start_date>='" + self.start_date + "' and start_date<='" + self.end_date + "' ) or (start_date<='" + self.start_date + "' and end_date>='" + self.start_date + "' ) or (end_date>='" + self.start_date + "' and end_date<='" + self.end_date + "' )) and ((('2001-01-01 '||start_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||start_time)::timestamp <= '2001-01-01 " + self.end_time + "' ) or (('2001-01-01 '||end_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||end_time)::timestamp <= '2001-01-01 " + self.end_time + "' ) or (('2001-01-01 '||end_time)::timestamp >= '2001-01-01 " + self.start_time + "' and ('2001-01-01 '||start_time)::timestamp <= '2001-01-01 " + self.start_time + "' ))")
        ids=[]
        for record in self._cr.fetchall():
            ids.append(record[0])
        return ids

    def copy(self, cr, uid, id, default=None, context=None):
        raise osv.except_osv(_('Forbbiden to duplicate'), _('Not possible to duplicate the record, please create a new one.'))

    @api.one
    def sendMail(self,id):
        global reservationmailsent
        template = self.env.ref('firedirect.email_template_reservation2', False)
        if template:
            for k,v in self.env.prefetch.items():
                self.env.prefetch[k]=set([id])
            if reservationmailsent!=id:
                reservationmailsent=id
                mail_message = template.send_mail(id)
            self.env.prefetch[k]=v

class firedirect_dreport(models.Model):
    _name = "firedirect.daily.report"
    _description = "Daily Report"
    date = fields.Date('Date', required=True)
    reservations = fields.Many2many('firedirect.reservation','fd_daily_report','report_id','res_id')
    
    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date']:
            raise model.except_model(_('Error!'), _('You have to select the date and try again.'))
        
        datas=self.pool.get('firedirect.reservation').search(cr,uid,[('start_date','<=',data['date']),('end_date','>=',data['date'])])
        
        cr.execute("delete from fd_daily_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_daily_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_dailyview',
            'report_type': 'qweb-pdf',
            }

    def show_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date']:
            raise model.except_model(_('Error!'), _('You have to select the date and try again.'))
        
        datas=self.pool.get('firedirect.reservation').search(cr,uid,[('start_date','<=',data['date']),('end_date','>=',data['date'])])
        
        cr.execute("delete from fd_daily_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_daily_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_dailyview',
            'report_type': 'qweb-html',
            }

class firedirect_attendance(models.TransientModel):
    _name = "firedirect.attendance"
    _description = "Attendance Report Wizard"
    _log_access = True
    date = fields.Date('Date', required=True)
    company_id = fields.Many2one('res.partner',  string='Company', required=True, domain=[('customer','=',True),('is_company','=',True)])
    course_id = fields.Many2one('firedirect.course',  string='Course', required=True)
    room_id = fields.Many2one('firedirect.room',  string='Room', required=True)
    reservations = fields.Many2many('firedirect.reservation','fd_att_report','report_id','res_id')
    atts = fields.Many2many('firedirect.att','fd_attt_report','report_id','att_id')
        
    
    def show_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date']:
            raise model.except_model(_('Error!'), _('You have to select the date and try again.'))
        if not data['company_id']:
            raise model.except_model(_('Error!'), _('You have to select the company and try again.'))
        if not data['course_id']:
            raise model.except_model(_('Error!'), _('You have to select the course and try again.'))
        if not data['room_id']:
            raise model.except_model(_('Error!'), _('You have to select the room and try again.'))

        cr.execute("select distinct r.id from firedirect_reservation as r,firedirect_reservation_student as rs, firedirect_student as s where start_date<='"+data['date']+"' and end_date>='"+data['date']+"' and r.id=rs.reservtion_id and s.id=rs.student_id and s.company_id="+str(data['company_id'][0])+" and r.course_id="+str(data['course_id'][0])+" and r.room_id="+str(data['room_id'][0]))
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_attt_report where report_id="+str(data['id']))
        cr.execute("delete from fd_att_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_att_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")
            
            cr.execute("select distinct a.id from firedirect_att as a where a.reservation_id="+str(id))
            atts = map(lambda x : x[0],cr.fetchall())
            for att in atts:
                cr.execute("insert into fd_attt_report (report_id,att_id) values ("+str(data['id'])+", "+str(att)+")")
                

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_attendance_view',
            'report_type': 'qweb-html',
            }        
        
    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date']:
            raise model.except_model(_('Error!'), _('You have to select the date and try again.'))
        if not data['company_id']:
            raise model.except_model(_('Error!'), _('You have to select the company and try again.'))
        if not data['course_id']:
            raise model.except_model(_('Error!'), _('You have to select the course and try again.'))
        if not data['room_id']:
            raise model.except_model(_('Error!'), _('You have to select the room and try again.'))

        cr.execute("select distinct r.id from firedirect_reservation as r,firedirect_reservation_student as rs, firedirect_student as s where start_date<='"+data['date']+"' and end_date>='"+data['date']+"' and r.id=rs.reservtion_id and s.id=rs.student_id and s.company_id="+str(data['company_id'][0])+" and r.course_id="+str(data['course_id'][0])+" and r.room_id="+str(data['room_id'][0]))
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_attt_report where report_id="+str(data['id']))
        cr.execute("delete from fd_att_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_att_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")
            
            cr.execute("select distinct a.id from firedirect_att as a where a.reservation_id="+str(id))
            atts = map(lambda x : x[0],cr.fetchall())
            for att in atts:
                cr.execute("insert into fd_attt_report (report_id,att_id) values ("+str(data['id'])+", "+str(att)+")")
                

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_attendance_view',
            'report_type': 'qweb-pdf',
            }


class firedirect_companyr(models.TransientModel):
    _name = "firedirect.company.report"
    _description = "Company Report Wizard"
    _log_access = True
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    company_id = fields.Many2one('res.partner',  string='Company', domain=[('customer','=',True),('is_company','=',True)])
    course_id = fields.Many2one('firedirect.course',  string='Course')
    reservations = fields.Many2many('firedirect.reservation','fd_comp_report','report_id','res_id')
        
    def show_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        query="select distinct r.id from firedirect_reservation as r,firedirect_reservation_student as rs, firedirect_student as s where r.id=rs.reservtion_id and s.id=rs.student_id "
        if(data['start_date']):
            query=query+"and start_date>='"+data['start_date']+"' "
        if(data['end_date']):
            query=query+"and end_date<='"+data['end_date']+"' "
        if(data['company_id']):
            query=query+"and s.company_id="+str(data['company_id'][0])+" "
        if(data['course_id']):
            query=query+"and r.course_id="+str(data['course_id'][0])+" "

        cr.execute(query)
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_comp_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_comp_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_company_view',
            'report_type': 'qweb-html',
            }

    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        query="select distinct r.id from firedirect_reservation as r,firedirect_reservation_student as rs, firedirect_student as s where r.id=rs.reservtion_id and s.id=rs.student_id "
        if(data['start_date']):
            query=query+"and start_date>='"+data['start_date']+"' "
        if(data['end_date']):
            query=query+"and end_date<='"+data['end_date']+"' "
        if(data['company_id']):
            query=query+"and s.company_id="+str(data['company_id'][0])+" "
        if(data['course_id']):
            query=query+"and r.course_id="+str(data['course_id'][0])+" "

        cr.execute(query)
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_comp_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_comp_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_company_view',
            'report_type': 'qweb-pdf',
            }


class firedirect_instructorr(models.TransientModel):
    _name = "firedirect.instructor.report"
    _description = "Instructor Report Wizard"
    _log_access = True
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    instructor_id = fields.Many2one('hr.employee',  string='Instructor', domain=[('job_id','=','Instructor')])
    reservations = fields.Many2many('firedirect.reservation','fd_inst_report','report_id','res_id')
        
    def show_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        query="select r.id from firedirect_reservation as r where True "
        if(data['start_date']):
            query=query+"and start_date>='"+data['start_date']+"' "
        if(data['end_date']):
            query=query+"and end_date<='"+data['end_date']+"' "
        if(data['instructor_id']):
            query=query+"and r.instructor_id="+str(data['instructor_id'][0])+" "

        cr.execute(query)
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_inst_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_inst_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_instructor_view',
            'report_type': 'qweb-html',
            }

    def print_report(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        
        query="select r.id from firedirect_reservation as r where True "
        if(data['start_date']):
            query=query+"and start_date>='"+data['start_date']+"' "
        if(data['end_date']):
            query=query+"and end_date<='"+data['end_date']+"' "
        if(data['instructor_id']):
            query=query+"and r.instructor_id="+str(data['instructor_id'][0])+" "

        cr.execute(query)
        datas = map(lambda x : x[0],cr.fetchall())
       
        cr.execute("delete from fd_inst_report where report_id="+str(data['id']))
        for id in datas:
            cr.execute("insert into fd_inst_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_instructor_view',
            'report_type': 'qweb-pdf',
            }


class firedirect_formr(models.TransientModel):
    _name = "firedirect.form.report"
    _inherit = ['mail.thread']
    _description = "Form Report Wizard"
    _log_access = True
    report_date = fields.Date('Report Date: ', required=True)
    start_date = fields.Date('Start Date: ', required=True)
    end_date = fields.Date('to', required=True)
    company = fields.Char(string='Company Name: ', required=True)
    att = fields.Char(string='ATT: ', required=True)
    subject = fields.Char(string='Subject: ', required=True, readonly=True, default='Student Report')
    employee = fields.Char(string='Emplpyee ', required=True)
    employee_no = fields.Char(string='ID # ', required=True)
    booked_for = fields.Char(string='booked for', required=True)
    duration = fields.Integer(string='durartion', required=True)
    attended = fields.Integer(string='attended', required=True)
    failed = fields.Integer(string='failed to show up', required=True)
    course_id = fields.Many2one('firedirect.course',  string='Course', required=True)
#    reservations = fields.Many2many('firedirect.reservation','fd_inst_report','report_id','res_id')
    book_date = fields.Char(string='', required=False)
#    course = fields.Char(string='failed to show up', required=True)
        
    @api.onchange('start_date','end_date')
    def _onchange_date(self):
        if self.start_date:
            if self.end_date:
                self.book_date=str(self.start_date) + " to " +str(self.end_date)
            else:
                self.book_date=""
        else:
            self.book_date=""
#    @api.onchange('course_id')
#    def _onchange_date(self):
#        self.course=self.course_id.name
        
    def show_report(self, cr, uid, ids, context=None):
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'firedirect.report_form_view',
            'report_type': 'qweb-html',
        }

    @api.multi
    def print_report(self):
        return self.env['report'].get_action(self, 'firedirect.report_form_view')

#    def show_report(self, cr, uid, ids, context=None):
#        data = self.read(cr, uid, ids, context=context)[0]
#        
#        return {
#            'type': 'ir.actions.report.xml',
#            'report_name': 'firedirect.report_form_view',
#            'report_type': 'qweb-pdf',
#            }

    @api.multi
    def email_report(self):

        assert len(self) == 1, 'This option should only be used for a single id at a time.'
        template = self.env.ref('firedirect.email_template_student_report', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='firedirect.form.report',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }



class firedirect_instcal(models.TransientModel):
    _inherit = 'firedirect.reservation'
    _name = 'firedirect.instcal'


class Partner(models.Model):
    _inherit = 'res.partner'
    _defaults = {'customer':True}

class Instructor(models.Model):
    _inherit = 'hr.employee'
#    _defaults = {'job_id':'Instructor'}

    id_type = fields.Selection([('iqama','Iqama'),('passport','Passport'),('saudi_id','Saudi ID'),('staff_id','Staff ID')], 'Identification Type')
    course_ids = fields.Many2many('firedirect.course','instructor_course_rel','employee_id','course_id', string='Courses')
    visa_expiry = fields.Date('Visa Expirty')
    visa_expiry_sent = fields.Date('')
    
#    has_reservations = fields.Boolean(compute='_has_reservations')
    reservations = fields.One2many('firedirect.reservation','instructor_id')

    day_reservations = fields.Many2many('firedirect.reservation',compute='_reservations',store=False)
    is_free = fields.Boolean()#compute='_is_free'
    
    at = fields.Date(string = 'Day')
    busy_at = fields.Char(compute='_busy_at',store=False)

    @api.one
    @api.depends('reservations','at')
    def _reservations(self):
        for record in self:
            if record.at:
                record.day_reservations=record.reservations.search([('start_date','<=',record.at),('end_date','>=',record.at),('instructor_id','=',record.id)])
            else:
                record.day_reservations=record.reservations.search([('id','=',0)])

    @api.one
    @api.depends('day_reservations','at')
    def _busy_at(self):
        for record in self:
            ba=[]
            for res in record.day_reservations:
                ba.append(res.start_time+" to "+res.end_time)
            record.busy_at=', '.join(ba)
    
#    @api.one
#    @api.depends('is_free')
#    def _color(self):
#        if self.is_free:
#            self.color="bg-success"
#        else:
#            self.color="bg-danger"

#    @api.one
#    @api.depends('day_reservations')
#    def _is_free(self):
#        curtime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
#        curdate=datetime.datetime.now().strftime("%Y-%m-%d")
#        _logger.error("...time--: %r",curtime)
#        for record in self:#WRONG??
#            self._cr.execute("select count(*) as c from firedirect_reservation where ("+ curdate +"||start_time)::timestamp<='" + time + "' and ("+ curdate +"||end_time)::timestamp>='" + time+" and instructor_id="+record.id)
#            record.is_free=len(self._cr.fetchall())==0

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        search2=[]
        for sterm in args:
            if sterm[0] != 'at':
                search2.append(sterm)
        res = super(Instructor, self).search(search2, offset=offset, limit=limit, order=order, count=count)
        found = False
        for sterm in args:
            if sterm[0] == 'at':
                for obj in res:
                    obj.at = sterm[2]
                found=True
                break
        if not found:
            for obj in res:
                obj.at=False
                
#        curtime=datetime.now().strftime("%Y-%m-%d %H:%M")
#        curdate=datetime.now().strftime("%Y-%m-%d")
#        _logger.error("...time--: %r",curtime)
#        for obj in res:#WRONG??
#            _logger.error("select * from firedirect_reservation where ("+ curdate +"||start_time)::timestamp<='" + curtime + "' and ("+ curdate +"||end_time)::timestamp>='" + curtime+"' and instructor_id="+str(obj.id))
#            self._cr.execute("select * from firedirect_reservation where ('"+ curdate +" '||start_time)::timestamp<='" + curtime + "' and ('"+ curdate +" '||end_time)::timestamp>='" + curtime+"' and instructor_id="+str(obj.id))
#            obj.is_free=len(self._cr.fetchall())==0
#            _logger.error("...time--: %r - %r",obj.is_free,obj.id)

        return res
    
    
class firedirect_att(models.Model):
    _name = 'firedirect.att'

    student_id = fields.Many2one('firedirect.student', string='Student', required=True)
    reservation_id = fields.Many2one('firedirect.reservation', string='Reservation', required=True)
    date = fields.Date(string = 'Day', required=False)
    status = fields.Selection([('showed_up','Showed Up'),('absent','Absent'),('undefined','Undefined')], 'Status',required=True)
    day = fields.Char(string = 'Day', required=True)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        idfound=dfound=found=False
        day=False
        date=False
        args2=[]
        for sterm in args:
            if sterm[0] == 'day':
                day=sterm[2]
                found=True
            if sterm[0] == 'id':
                idfound=True
            if sterm[0] == 'date':
                date=sterm[2]
                dfound=True
            else:
                args2.append(sterm)
        if not found or not dfound:
            if idfound:
                args2=args
            else:
                args2=[('id','=',0)]
            return super(firedirect_att, self).search(args2, offset=offset, limit=limit, order=order, count=count)
        reservations = self.env['firedirect.reservation'].search([('start_date','<=',date),('end_date','>=',date)])
        for res in reservations:
            for stu in res.student_ids:
                self._cr.execute("select * from firedirect_att where student_id="+str(stu.id)+" and reservation_id="+str(res.id)+" and day='"+str(day)+"'")
                cnt=self._cr.fetchall()
                if len(cnt)==0:
                    self.create({'student_id':stu.id,'reservation_id':res.id,'day':day,'date':date,'status':'undefined'})
        return super(firedirect_att, self).search(args2, offset=offset, limit=limit, order=order, count=count)

class firedirect_attw(models.TransientModel):
    _name = "firedirect.attw"
    _description = "Attendance Wizard"
    _log_access = True
    date = fields.Date('Date', required=True)
    course_id = fields.Many2one('firedirect.course',  string='Course', required=True)
    room_id = fields.Many2one('firedirect.room',  string='Room', required=True)
    reservation_id = fields.Many2one('firedirect.reservation','Reservation',required=True, domain=[])
    day = fields.Many2one('firedirect.day','Day',required=True, domain=[])
        
    @api.onchange('course_id','room_id','date')
    def _update_reservation(self):
        ddomain=[('id','=','0')]
        rdomain=[('id','=','0')]
        if self.course_id:
            self._update_days(self.course_id.duration)
            ddomain=[('day_no','<=',self.course_id.duration)]
            if self.room_id:
                if self.date:
                    rdomain = [('course_id', '=', self.course_id.id),('room_id', '=', self.room_id.id),('start_date','<=',self.date),('end_date','>=',self.date)]
        self.reservation_id=False
        self.day=False
        return {'domain': {'reservation_id': rdomain,'day':ddomain}}
    
    def _update_days(self,number):
        self.env['firedirect.day'].search([('day_no','<=',number)])

    def dosearch(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids, context=context)[0]
        if not data['date']:
            raise model.except_model(_('Error!'), _('You have to select the date and try again.'))
        if not data['reservation_id']:
            raise model.except_model(_('Error!'), _('You have to select the reservation and try again.'))
        if not data['day']:
            raise model.except_model(_('Error!'), _('You have to select the day and try again.'))
        if not data['course_id']:
            raise model.except_model(_('Error!'), _('You have to select the course and try again.'))
        if not data['room_id']:
            raise model.except_model(_('Error!'), _('You have to select the room and try again.'))

#        cr.execute("select distinct r.id from firedirect_reservation as r,firedirect_reservation_student as rs, firedirect_student as s where start_date<='"+data['date']+"' and end_date>='"+data['date']+"' and r.id=rs.reservtion_id and s.id=rs.student_id and s.company_id="+str(data['company_id'][0])+" and r.course_id="+str(data['course_id'][0])+" and r.room_id="+str(data['room_id'][0]))
#        datas = map(lambda x : x[0],cr.fetchall())
       
#        cr.execute("delete from fd_att_report where report_id="+str(data['id']))
#        for id in datas:
#            cr.execute("insert into fd_att_report (report_id,res_id) values ("+str(data['id'])+", "+str(id)+")")

        return {
        'name':_("Attendance"),#Name You want to display on wizard
        'view_mode': 'tree',
#        'view_id': view_id
        'view_type': 'form',
        'res_model': 'firedirect.att',# With . Example sale.order
        'type': 'ir.actions.act_window',
#        'target': 'default',
        'domain': [('reservation_id','=',data['reservation_id'][0]),('day','=',data['day'][1]),('date','=',data['date'])],
#        'context': {'reservation_id':data['reservation_id'][0],'day':data['day'][1],'date':data['date']}
        }


class firedirect_day(models.Model):
    _name = "firedirect.day"
    _description = "Day NO"
    _rec_name = 'day_no'

    day_no = fields.Integer(string='Day NO', required=True)
    
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        found=False
        no = 0
        for sterm in args:
            if sterm[0] == 'day_no':
                no=sterm[2]
                found=True

        if not found:
            args.append(('day_no','=',0))
        for i in range(1,no):
            self._cr.execute("select * from firedirect_day where day_no="+str(i))
            cnt=self._cr.fetchall()
            if len(cnt)==0:
                self.create({'day_no':i})
        return super(firedirect_day, self).search(args, offset=offset, limit=limit, order=order, count=count)
        
#class firedirect_config_settings(models.TransientModel):
#    _name = 'firedirect.config.settings'
#    _inherit = 'res.config.settings'
#    email_reservation = fields.Many2one('email.template', string='Reservtion Confirmation Email')
#    email_expiring_visa = fields.Many2one('email.template', string='Expiring Visa Email')
#    email_address = fields.Char('Email Address')
    
class firedirect_user(models.Model):
    _inherit = "res.users"
    
    _defaults = {'display_employees_suggestions':False,'alias_domain':False}
    
#class firedirect_holidays(models.Model):
#    _inherit = "hr.holidays"
#    
#    reservation_ids=fields.Many2one('firedirect.reservation','Reservations',compute='_get_reservations',store=False)
#    
#    @api.one
#    @api.depends('date_from','date_to','employee_id')
#    def _get_reservations(self):
#        self._cr.execute("select id from firedirect_reservation where instructor_id = " + str(self.employee_id) + " and ((start_date>='" + self.date_from + "' and start_date<='" + self.date_to + "' ) or (start_date<='" + self.date_from + "' and end_date>='" + self.date_from + "' ) or (end_date>='" + self.date_from + "' and end_date<='" + self.date_to + "' ))")
#        ids = map(lambda x : x[0],self._cr.fetchall())
#        return ids
        
    
class mail_notification(osv.Model):
    _inherit = 'mail.notification'
    
    def get_signature_footer(self, cr, uid, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        footer = ""
        if not user_id:
            return footer
        return ''
    
        # add user signature
        user = self.pool.get("res.users").browse(cr, SUPERUSER_ID, [user_id], context=context)[0]
        if user_signature:
            if user.signature:
                signature = user.signature
            else:
                signature = "--<br />%s" % user.name
            footer = tools.append_content_to_html(footer, signature, plaintext=False)

        # add company signature
        if user.company_id.website:
            website_url = ('http://%s' % user.company_id.website) if not user.company_id.website.lower().startswith(('http:', 'https:')) \
                else user.company_id.website
            company = "<a style='color:inherit' href='%s'>%s</a>" % (website_url, user.company_id.name)
        else:
            company = user.company_id.name
        sent_by = _('Sent by %(company)s using %(odoo)s')

        signature_company = ''

        footer = tools.append_content_to_html(footer, signature_company, plaintext=False, container_tag='div')

        return footer
    