# -*- coding: utf-8 -*-
# Copyright 2017 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import random
import string

from odoo import api, fields, models, _
import  logging

log = logging.getLogger(__name__)

TOKEN_LENGHT = 32

class AuthApiToken(models.Model):

    _name = 'auth.api.token'
    _description = 'Auth Api Token'

    def _default_user_id(self):
        return self.env.user

    user_id = fields.Many2one(
        'res.users', 
        string=_('User'),
        required=True,
        default=_default_user_id
    )

    token = fields.Char(
        string=_("API Key"),
        readonly=True
    )

    @api.model
    def retrieve_from_user(self, user_id):
        keys = self.search([('user_id', '=', user_id.id)])
        if len(keys) > 0:
            return keys[0]
        
        key = self.create({
            'user_id': user_id.id
        })

        return key

    @api.model
    def retrieve_from_api_key(self, api_key):

        keys = self.search([
            ('token', '=', api_key)
        ])

        if len(keys) > 0:
            return keys[0]

        return False

    def _generate_token(self):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(TOKEN_LENGHT))

    @api.model
    def create(self, vals):
        vals['token'] = self._generate_token()
        return super(AuthApiToken, self).create(vals)