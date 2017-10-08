# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################
{
    "name": "MRP Production edit",
    "version": "10.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "price": 20.0,
    "currency": 'EUR',
    'description': """
    Allow editing of MRP Orders created from empty BoM,

    To use this module you must define empty BoM for products that

    you want to edit its generated MO.
    """,
    "author": "DVIT.ME",
    "website": "http://dvit.me",
    "depends": ['mrp','dvit_product_cost_bom_auto'],
    "data": ["views/mrp_production_view.xml"],
    "installable": True,
}
