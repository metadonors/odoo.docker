# -*- coding: utf-8 -*-
{
    'name': "Orari di lavoro archiviabili",
    'summary': "Aggiunge il flag Attivo agli orari di lavoro (resource.calendar)",
    'description': """
Orari di lavoro archiviabili
============================

Il modello ``resource.calendar`` di Odoo 12 non ha il campo ``active``: una
tipologia di orario creata una volta resta per sempre nelle tendine di scelta
del contratto e del dipendente.

Questo modulo aggiunge ``active`` (default ``True``, quindi tutti gli orari
esistenti restano attivi) piu' le viste per archiviare e ripristinare.

Archiviare un orario che ha ancora contratti attivi e' impedito: e' il caso
che genera dati incoerenti a valle.
""",
    'version': '12.0.1.0.0',
    'category': 'Human Resources',
    'author': "Metadonors",
    'website': "https://www.metadonors.it",
    'license': 'LGPL-3',
    'depends': [
        'resource',
        'hr_contract',
    ],
    'data': [
        'views/resource_calendar_views.xml',
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
    'application': False,
    'auto_install': False,
}
