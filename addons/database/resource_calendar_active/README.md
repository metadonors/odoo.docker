# Orari di lavoro archiviabili (`resource_calendar_active`)

Odoo 12, `workplace.metadonors.it`.

## Perche'

`resource.calendar` in Odoo 12 non ha il campo `active`: le tipologie di orario
create restano per sempre nelle tendine. In produzione sono 134 e non c'e' modo
di togliere quelle non piu' in uso. Si vede in tre posti: la scelta dell'orario
sul contratto in Odoo, MetaContractFlow, la pagina `/operations/orari` di ONE.

## Cosa fa

- Aggiunge `active` a `resource.calendar` (default `True`).
- Form: campo **Attivo** accanto a *Ore al giorno*.
- Lista: `active` nell'arch (accende **Archivia**/**Ripristina** nel menu
  Azione) e righe archiviate in grigio.
- Ricerca: filtro **Archiviati**.
- Impedisce di archiviare un orario ancora in uso:
  - contratti vivi (`hr.contract` non archiviato, stato `open` o `pending`,
    `date_end` nullo o futuro) che puntano all'orario;
  - orario usato come orario predefinito di un'azienda (`res.company.
    resource_calendar_id`): finirebbe sui contratti nuovi pur non essendo piu'
    scegliibile.

Nessun orario viene archiviato dall'installazione: la pulizia la fa HR caso per
caso, dopo.

## `active` non e' un campo inerte

In Odoo l'ORM filtra da solo i record archiviati in ogni `search` e in ogni
tendina. Le tre conseguenze che contano, tutte coperte dai test in `tests/`:

1. **Un contratto che punta a un orario archiviato continua a mostrarlo.**
   La lettura di un many2one non passa da `search`: `name_get` viene chiamato
   sugli id gia' noti, `active_test` non c'entra.
2. **Le ricerche e i raggruppamenti HR per orario non perdono righe.**
   Quando un dominio attraversa un many2one (`resource_calendar_id.name`)
   l'ORM espande la foglia con `active_test=False`
   (`odoo/osv/expression.py`, 12.0). Stesso discorso per `read_group`, che
   risolve le etichette per id.
3. **L'orario archiviato sparisce dalle tendine** di `hr.contract` e
   `hr.employee`, che e' lo scopo dell'intervento.

## Verifica su istanza di prova (non in produzione)

Dopo `-u resource_calendar_active`:

```sql
select count(*) from resource_calendar where active is not true;  -- deve dare 0
```

Test automatici:

```
odoo -d <db_di_prova> -i resource_calendar_active --test-enable --stop-after-init
```

A mano, dall'interfaccia:

1. Archivia un orario a zero contratti: sparisce dalla lista e dalle tendine di
   contratto e dipendente, torna visibile col filtro **Archiviati**.
2. Prova ad archiviare un orario con contratti attivi: deve fermarsi con
   l'elenco delle persone coinvolte.
3. Riapri due o tre contratti esistenti: l'orario si vede, il campo non e'
   vuoto e non c'e' errore.

## Fuori perimetro

- La query Redash 225 *MTD Orari dipendenti* legge la tabella in SQL grezzo:
  continuera' a vedere anche gli archiviati. Adeguare i consumatori a valle
  (MCF, ONE) e' lavoro separato.
- Nessun orario viene archiviato da questo modulo.
