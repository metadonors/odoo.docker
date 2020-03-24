
import logging
import json

from odoo import http
from odoo.http import request, Response, AuthenticationError
from odoo.exceptions import AccessDenied

log = logging.getLogger()

class ApiAuthController(http.Controller):
    @http.route(['/api/auth/token'], methods=['POST'], type='json', csrf=False, auth="public")
    def request_api_key(self, **kw):
        try:
            data = json.loads(str(request.httprequest.data.decode('utf-8')))
        except:
            raise AuthenticationError()
        
        uid = request.env['res.users'].sudo()._login(request.db, data['login'], data['password'])
        if not uid:
            raise AuthenticationError()
        
        user_id = request.env['res.users'].sudo().browse(uid)
        api_key_id = request.env['auth.api.token'].sudo().retrieve_from_user(user_id)

        response = {"auth_token": api_key_id.token}

        return response