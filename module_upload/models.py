# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
import zipfile
import os


class upload_module(models.Model):
    _name = 'upload.module'

    name = fields.Char(string="Module Name")
    list_of_addons_paths = tools.config['addons_path'].split(",")
    nlist_path = []
    for path in list_of_addons_paths:
        nlist_path.append((path, path))
    addons_paths = fields.Selection(nlist_path,
        string="Add-ons Paths", help="Please choose one of these directories to put "
                                     "your module in",
        required=True)

    binary_field = fields.Char('Module File')


    @api.model
    def create(self, values):
        try:
            path_to_zip_file = values['binary_field']
            directory_to_extract_to = values['addons_paths']
            values['name'] = values['binary_field'].split("/")[-1].split(".")[0]
            zip_ref = zipfile.ZipFile(path_to_zip_file, 'r')
            zip_ref.extractall(directory_to_extract_to)
            zip_ref.close()
        except Exception as e:
            print e
        new_id = super(upload_module, self).create(values)
        return new_id