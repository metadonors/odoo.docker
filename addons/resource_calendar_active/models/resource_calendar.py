# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError

# Stati in cui un contratto e' considerato vivo: sta girando o e' da rinnovare.
LIVE_CONTRACT_STATES = ['open', 'pending']

# Quanti contratti elencare nel messaggio di errore prima di troncare.
CONTRACTS_IN_MESSAGE = 5


class ResourceCalendar(models.Model):
    _inherit = 'resource.calendar'

    active = fields.Boolean(
        string="Attivo",
        default=True,
        index=True,
        help="Un orario archiviato resta sui contratti che lo usano gia', "
             "ma sparisce dalle tendine di scelta di contratti e dipendenti.",
    )

    @api.multi
    def write(self, vals):
        if 'active' in vals and not vals['active']:
            # Solo gli orari che stanno passando da attivo ad archiviato:
            # riscrivere active=False su un orario gia' archiviato e' innocuo.
            self.filtered('active')._check_archivable()
        return super(ResourceCalendar, self).write(vals)

    @api.multi
    def _check_archivable(self):
        """Blocca l'archiviazione degli orari ancora in uso.

        Due casi, entrambi generano dati incoerenti a valle:
        contratti vivi che puntano all'orario, e orario usato come default
        aziendale (finirebbe sui contratti nuovi pur non essendo scegliibile).
        """
        for calendar in self:
            contracts = calendar._live_contracts()
            if contracts:
                raise UserError(calendar._archive_blocked_message(contracts))
            companies = calendar._companies_defaulting_here()
            if companies:
                raise UserError(_(
                    "Non puoi archiviare l'orario «%s»: e' l'orario di lavoro "
                    "predefinito di %s.\n\n"
                    "Cambia prima il predefinito dell'azienda, poi archivia."
                ) % (calendar.name, ", ".join(companies.mapped('name'))))

    @api.multi
    def _live_contracts(self):
        """Contratti attivi, in corso o da rinnovare, che usano questo orario.

        ``search`` esclude da solo i contratti archiviati (hr.contract ha
        ``active``), quindi il filtro non va ripetuto nel dominio.
        """
        self.ensure_one()
        today = fields.Date.context_today(self)
        return self.env['hr.contract'].sudo().search([
            ('resource_calendar_id', '=', self.id),
            ('state', 'in', LIVE_CONTRACT_STATES),
            '|', ('date_end', '=', False), ('date_end', '>=', today),
        ])

    @api.multi
    def _companies_defaulting_here(self):
        self.ensure_one()
        return self.env['res.company'].sudo().search([
            ('resource_calendar_id', '=', self.id),
        ])

    @api.multi
    def _archive_blocked_message(self, contracts):
        self.ensure_one()
        righe = []
        for contract in contracts[:CONTRACTS_IN_MESSAGE]:
            persona = contract.employee_id.name or _("senza dipendente")
            righe.append(u"- %s (%s)" % (persona, contract.name))
        if len(contracts) > CONTRACTS_IN_MESSAGE:
            righe.append(_("- e altri %s") % (len(contracts) - CONTRACTS_IN_MESSAGE))
        return _(
            "Non puoi archiviare l'orario «%s»: ci sono ancora %s contratti "
            "attivi che lo usano.\n\n%s\n\n"
            "Sposta prima quei contratti su un altro orario, poi archivia."
        ) % (self.name, len(contracts), "\n".join(righe))
