# -*- coding: utf-8 -*-
# Copyright 2017 Metadonors Srl
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Auth Api Key',
    'description': """
        Authentication with Api Key in headers""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Metadonors Srl',
    'website': 'https://www.metadonors.it',
    'depends': [
        'auth_lpi'
    ],
    'data': [
        'security/auth_api_token.xml',
        'views/auth_api_token.xml',
    ],
    'demo': [
    ],
}
