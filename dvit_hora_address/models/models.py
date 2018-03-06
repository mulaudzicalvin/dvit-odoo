# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    building_id= fields.Many2one("res.zone.building", string="Buliding" )
    country_id = fields.Many2one(comodel_name="res.country", string="Country", required=True, )
    city_id = fields.Many2one(comodel_name="res.country.city", string="City", required=True, )
    zone_id = fields.Many2one(comodel_name="res.country.city.zone", string="Zone", required=True, )
    floor = fields.Char(string="Floor" )

class ResCountryState(models.Model):
    _inherit = 'res.country.state'
    city_ids = fields.One2many(
        string="Cities",
        comodel_name="res.country.city",
        inverse_name="state_id",
    )

class ResCountryCity(models.Model):
    _name = 'res.country.city'
    name = fields.Char("City",required=True)
    state_id = fields.Many2one(comodel_name="res.country.state", string="state", required=True, )
    zip_code = fields.Integer("Zip",size=5)
    zone_ids = fields.One2many(
        string="Zones",
        comodel_name="res.country.city.zone",
        inverse_name="city_id",
    )

class ResCountryCityZone(models.Model):
    _name = 'res.country.city.zone'
    city_id = fields.Many2one(comodel_name="res.country.city", string="City", required=True, )
    name = fields.Char("Zone",required=True)
    sequence = fields.Integer("Sequence")
    building_ids = fields.One2many(
        string="Buildings",
        comodel_name="res.zone.building",
        inverse_name="zone_id",
    )

class ResZoneBuilding(models.Model):
    _name = 'res.zone.building'
    name = fields.Char('Building No.',required=True)
    zone_id = fields.Many2one(comodel_name="res.country.city.zone", string="Zone" , required=True)
    sequence =fields.Integer("Sequence", default=None, required=True)
