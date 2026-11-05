# PersonalExpenseSystem

Sistema console per la gestione delle spese personali e dei budget mensili (Python + SQLite).

## Requisiti
- Python 3.10 o superiore (serve `match/case`)
- Nessuna libreria esterna: si usano solo i moduli standard `sqlite3`, `os`, `datetime`

## Esecuzione
Dalla cartella principale del progetto:

```bash
python src/main.py
```

(su alcuni sistemi il comando è `python3 src/main.py`)

Al primo avvio il programma crea `src/spese.db` eseguendo `sql/database.sql`
(tabelle, vincoli e dati di esempio). Per ripartire da zero basta cancellare `src/spese.db`.

## Struttura
- `src/main.py` – programma
- `sql/database.sql` – creazione tabelle, vincoli e dati di esempio
- `demo/demo_video.mp4` – video dimostrativo
