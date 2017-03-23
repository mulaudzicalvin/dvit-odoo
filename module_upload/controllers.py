# -*- coding: utf-8 -*-
from openerp import http, tools
import werkzeug
import os
from openerp.addons.web.controllers.main import content_disposition


class upload_module(http.Controller):
    @http.route('/upload_module', auth='user')
    def index(self, **kw):
        try:
            uploaded_file = kw['uploaded_file']
            uploaded_file.save(os.path.join(tools.config["data_dir"], uploaded_file.filename))
            return http.request.make_response(os.path.join(tools.config["data_dir"], uploaded_file.filename))
        except Exception as e:
            print e

    @http.route('/download/<name>',auth='user')
    def download(self, name, **kw):
        try:
            file_to_download = open(name.replace("'", "/"))
            return http.request.make_response(file_to_download,
                [('Content-Type', 'application/octet-stream'),
                ('Content-Disposition', content_disposition(name.split("'")[-1]))])
        except Exception as e:
            print e