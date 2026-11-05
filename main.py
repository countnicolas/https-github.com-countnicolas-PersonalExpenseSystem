"""Sistema di Gestione delle Spese Personali e del Budget (console + SQLite)."""
import os
import sqlite3
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(BASE, "..", "sql", "database.sql")
DB_FILE = os.path.join(BASE, "spese.db")


def connetti():
    """Apre il database; se è nuovo esegue lo script SQL di creazione."""
    nuovo = not os.path.exists(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON")
    if nuovo:
        with open(SQL_FILE, encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()
    return conn


def leggi_numero(messaggio):
    try:
        return float(input(messaggio).strip().replace(",", "."))
    except ValueError:
        return None


def data_valida(testo, formato):
    try:
        datetime.strptime(testo, formato)
        return True
    except ValueError:
        return False


def trova_categoria(conn, nome):
    return conn.execute(
        "SELECT id_categoria FROM categorie WHERE nome = ?", (nome,)
    ).fetchone()


# ---------------- MODULO 1 ----------------
def gestione_categorie(conn):
    nome = input("Nome della categoria: ").strip()
    if nome == "":
        print("Errore: il nome non può essere vuoto.")
        return
    if trova_categoria(conn, nome):
        print("La categoria esiste già.")
        return
    conn.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
    conn.commit()
    print("Categoria inserita correttamente.")


# ---------------- MODULO 2 ----------------
def inserisci_spesa(conn):
    data = input("Data (YYYY-MM-DD): ").strip()
    importo = leggi_numero("Importo: ")
    nome = input("Nome della categoria: ").strip()
    descrizione = input("Descrizione (facoltativa): ").strip()

    if not data_valida(data, "%Y-%m-%d"):
        print("Errore: formato data non valido (usare YYYY-MM-DD).")
        return
    if importo is None or importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    cat = trova_categoria(conn, nome)
    if not cat:
        print("Errore: la categoria non esiste.")
        return
    conn.execute(
        "INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)",
        (data, importo, cat[0], descrizione or None),
    )
    conn.commit()
    print("Spesa inserita correttamente.")


# ---------------- MODULO 3 ----------------
def definisci_budget(conn):
    mese = input("Mese (YYYY-MM): ").strip()
    nome = input("Nome della categoria: ").strip()
    importo = leggi_numero("Importo del budget: ")

    if not data_valida(mese, "%Y-%m"):
        print("Errore: formato mese non valido (usare YYYY-MM).")
        return
    if importo is None or importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return
    cat = trova_categoria(conn, nome)
    if not cat:
        print("Errore: la categoria non esiste.")
        return
    conn.execute(
        """INSERT INTO budget (mese, id_categoria, importo) VALUES (?, ?, ?)
           ON CONFLICT(mese, id_categoria) DO UPDATE SET importo = excluded.importo""",
        (mese, cat[0], importo),
    )
    conn.commit()
    print("Budget mensile salvato correttamente.")


# ---------------- MODULO 4 ----------------
def report_totale_categoria(conn):
    righe = conn.execute(
        """SELECT c.nome, COALESCE(SUM(s.importo), 0)
           FROM categorie c LEFT JOIN spese s ON s.id_categoria = c.id_categoria
           GROUP BY c.id_categoria ORDER BY c.nome"""
    ).fetchall()
    print(f"\n{'Categoria':<20}{'Totale Speso':>12}")
    print("-" * 32)
    for nome, tot in righe:
        print(f"{nome:<20}{tot:>12.2f}")


def report_mensile_budget(conn):
    righe = conn.execute(
        """SELECT b.mese, c.nome, b.importo,
                  COALESCE((SELECT SUM(s.importo) FROM spese s
                            WHERE s.id_categoria = b.id_categoria
                              AND substr(s.data, 1, 7) = b.mese), 0)
           FROM budget b JOIN categorie c ON c.id_categoria = b.id_categoria
           ORDER BY b.mese, c.nome"""
    ).fetchall()
    if not righe:
        print("Nessun budget definito.")
        return
    for mese, nome, budget, speso in righe:
        if speso > budget:
            stato = "SUPERAMENTO BUDGET"
        else:
            stato = "Nel budget"
        print(f"\nMese: {mese}\nCategoria: {nome}\nBudget: {budget:g}\n"
              f"Speso: {speso:g}\nStato: {stato}")


def report_elenco_spese(conn):
    righe = conn.execute(
        """SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '')
           FROM spese s JOIN categorie c ON c.id_categoria = s.id_categoria
           ORDER BY s.data, s.id_spesa"""
    ).fetchall()
    print(f"\n{'Data':<12}{'Categoria':<16}{'Importo':>10}  Descrizione")
    print("-" * 62)
    for data, nome, imp, desc in righe:
        print(f"{data:<12}{nome:<16}{imp:>10.2f}  {desc}")


def menu_report(conn):
    while True:
        print("\n--- MENU REPORT ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese ordinate per data")
        print("4. Ritorna al menu principale")
        scelta = input("Inserisci la tua scelta: ").strip()
        match scelta:
            case "1":
                report_totale_categoria(conn)
            case "2":
                report_mensile_budget(conn)
            case "3":
                report_elenco_spese(conn)
            case "4":
                return
            case _:
                print("Scelta non valida. Riprovare.")


# ---------------- MENU PRINCIPALE ----------------
def main():
    conn = connetti()
    print("Benvenuto nel Sistema Spese Personali!")
    while True:
        print("\n-------------------------")
        print("SISTEMA SPESE PERSONALI")
        print("-------------------------")
        print("1. Gestione Categorie")
        print("2. Inserisci Spesa")
        print("3. Definisci Budget Mensile")
        print("4. Visualizza Report")
        print("5. Esci")
        print("-------------------------")
        try:
            scelta = input("Inserisci la tua scelta: ").strip()
        except EOFError:
            break
        match scelta:
            case "1":
                gestione_categorie(conn)
            case "2":
                inserisci_spesa(conn)
            case "3":
                definisci_budget(conn)
            case "4":
                menu_report(conn)
            case "5":
                print("Arrivederci!")
                break
            case _:
                print("Scelta non valida. Riprovare.")
    conn.close()


if __name__ == "__main__":
    main()
