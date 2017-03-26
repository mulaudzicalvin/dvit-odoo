# -*- coding: utf-8 -*-

from openerp import models, fields, api
import subprocess


class model_script(models.Model):
    _name = 'model.script'
    name = fields.Char(string="Name", required=True, help="This is the name you will see and select to use this "
                                                          "script.")

    desc = fields.Char(string="Description")
    command = fields.Char(string="Command", required=True, help="Command to be executed.")
    command_args = fields.Char(string="Command Arguments", help="These are the arguments "
                                                                               "of executed command ")
    @api.multi
    def cmd_execute(self):
        for record in self:
            if self.command_args != False:
                subprocess.call([record.command, record.command_args])
            else:
                subprocess.call(record.command)
