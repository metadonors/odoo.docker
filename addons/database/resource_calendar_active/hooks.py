# -*- coding: utf-8 -*-
import logging

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    """Garantisce che nessun orario preesistente resti archiviato.

    L'ORM riempie da solo la nuova colonna con il default del campo
    (``True``), ma il controllo costa niente e rende l'esito verificabile:
    dopo l'update del modulo ``select count(*) from resource_calendar where
    active is not true`` deve dare 0.
    """
    cr.execute("UPDATE resource_calendar SET active = TRUE WHERE active IS NOT TRUE")
    if cr.rowcount:
        _logger.info("resource_calendar_active: %s orari riportati ad attivi", cr.rowcount)
