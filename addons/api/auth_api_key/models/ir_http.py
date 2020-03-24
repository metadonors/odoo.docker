# -*- coding: utf-8 -*-
# Copyright 2019 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import api, fields, models, _
from odoo.http import request
from odoo.exceptions import AccessDenied

_logger = logging.getLogger(__name__)

class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'
    
    @classmethod
    def _auth_method_api_key(cls):
        headers = request.httprequest.environ
        api_key = headers.get('HTTP_AUTHORIZATION')
        if api_key:
            api_key = api_key.replace('Token ', '')
            request.uid = 1
            auth_api_key = request.env['auth.api.token'].retrieve_from_api_key(
                api_key
            )
            if auth_api_key:
                # reset _env on the request since we change the uid...
                # the next call to env will instantiate an new
                # odoo.api.Environment with the user defined on the
                # auth.api_key
                request._env = None
                request.uid = auth_api_key.user_id.id
                request.auth_api_key = auth_api_key
                return True
        _logger.error("Wrong HTTP_API_KEY, access denied")
        raise AccessDenied()
