# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import common


class TestResourceCalendarActive(common.TransactionCase):

    def setUp(self):
        super(TestResourceCalendarActive, self).setUp()
        self.Calendar = self.env['resource.calendar']
        self.Contract = self.env['hr.contract']
        self.calendar = self.Calendar.create({'name': "Orario di prova"})
        self.employee = self.env['hr.employee'].create({'name': "Mario Rossi"})
        self.contract_type = self.env['hr.contract.type'].create({'name': "Prova"})

    def _contract(self, state='open', date_end=False, calendar=None):
        return self.Contract.create({
            'name': "Contratto %s" % state,
            'employee_id': self.employee.id,
            'type_id': self.contract_type.id,
            'wage': 1000.0,
            'state': state,
            'date_start': fields.Date.to_string(date.today() - timedelta(days=365)),
            'date_end': date_end,
            'resource_calendar_id': (calendar or self.calendar).id,
        })

    def test_10_nessun_orario_nasce_archiviato(self):
        self.assertTrue(self.calendar.active)
        self.cr.execute("SELECT count(*) FROM resource_calendar WHERE active IS NOT TRUE")
        self.assertEqual(
            self.cr.fetchone()[0], 0,
            "Dopo l'installazione del modulo nessun orario deve risultare archiviato",
        )

    def test_20_orario_senza_contratti_si_archivia(self):
        self.calendar.toggle_active()
        self.assertFalse(self.calendar.active)
        # Sparisce dalle tendine di scelta...
        trovati = self.Calendar.name_search("Orario di prova")
        self.assertNotIn(self.calendar.id, [x[0] for x in trovati])
        # ...ma resta visibile col filtro Archiviati.
        archiviati = self.Calendar.search([('active', '=', False)])
        self.assertIn(self.calendar, archiviati)

    def test_21_orario_archiviato_si_ripristina(self):
        self.calendar.toggle_active()
        self.calendar.toggle_active()
        self.assertTrue(self.calendar.active)
        trovati = self.Calendar.name_search("Orario di prova")
        self.assertIn(self.calendar.id, [x[0] for x in trovati])

    def test_30_contratto_in_corso_blocca(self):
        self._contract(state='open')
        with self.assertRaises(UserError):
            self.calendar.toggle_active()
        self.assertTrue(self.calendar.active)

    def test_31_contratto_da_rinnovare_blocca(self):
        self._contract(state='pending')
        with self.assertRaises(UserError):
            self.calendar.toggle_active()

    def test_32_contratto_con_scadenza_futura_blocca(self):
        self._contract(
            state='open',
            date_end=fields.Date.to_string(date.today() + timedelta(days=30)),
        )
        with self.assertRaises(UserError):
            self.calendar.toggle_active()

    def test_33_archiviazione_massiva_si_ferma_sul_primo_orario_in_uso(self):
        libero = self.Calendar.create({'name': "Orario libero"})
        self._contract(state='open')
        with self.assertRaises(UserError):
            (self.calendar + libero).write({'active': False})
        self.assertTrue(libero.active)

    def test_34_default_azienda_blocca(self):
        self.env.user.company_id.resource_calendar_id = self.calendar
        with self.assertRaises(UserError):
            self.calendar.toggle_active()

    def test_40_contratto_scaduto_non_blocca(self):
        self._contract(state='close')
        self.calendar.toggle_active()
        self.assertFalse(self.calendar.active)

    def test_41_contratto_con_data_fine_passata_non_blocca(self):
        self._contract(
            state='open',
            date_end=fields.Date.to_string(date.today() - timedelta(days=1)),
        )
        self.calendar.toggle_active()
        self.assertFalse(self.calendar.active)

    def test_42_contratto_archiviato_non_blocca(self):
        contratto = self._contract(state='open')
        contratto.active = False
        self.calendar.toggle_active()
        self.assertFalse(self.calendar.active)

    def test_50_il_contratto_continua_a_mostrare_l_orario_archiviato(self):
        self.calendar.toggle_active()
        contratto = self._contract(state='open')
        letto = contratto.read(['resource_calendar_id'])[0]['resource_calendar_id']
        self.assertEqual(letto[0], self.calendar.id)
        self.assertTrue(letto[1], "Il nome dell'orario archiviato deve restare leggibile")

    def test_60_le_ricerche_per_orario_non_perdono_righe(self):
        contratto = self._contract(state='open')
        self.calendar.toggle_active()
        self.assertIn(contratto, self.Contract.search([
            ('resource_calendar_id', '=', self.calendar.id),
        ]))
        self.assertIn(contratto, self.Contract.search([
            ('resource_calendar_id.name', '=', "Orario di prova"),
        ]))
        self.assertIn(contratto, self.Contract.search([
            ('resource_calendar_id', 'ilike', "Orario di prova"),
        ]))

    def test_61_i_raggruppamenti_per_orario_non_perdono_righe(self):
        contratto = self._contract(state='open')
        self.calendar.toggle_active()
        gruppi = self.Contract.read_group(
            [('id', '=', contratto.id)], ['wage'], ['resource_calendar_id'])
        self.assertEqual(len(gruppi), 1)
        self.assertEqual(gruppi[0]['resource_calendar_id'][0], self.calendar.id)
