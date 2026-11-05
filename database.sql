-- =====================================================
-- Sistema di Gestione delle Spese Personali e del Budget
-- Script di creazione del database (SQLite)
-- =====================================================

PRAGMA foreign_keys = ON;

CREATE TABLE categorie (
    id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,          -- PRIMARY KEY
    nome         TEXT NOT NULL UNIQUE                         -- NOT NULL + UNIQUE
                 CHECK (length(trim(nome)) > 0)               -- CHECK: nome non vuoto
);

CREATE TABLE spese (
    id_spesa     INTEGER PRIMARY KEY AUTOINCREMENT,           -- PRIMARY KEY
    data         TEXT NOT NULL                                -- NOT NULL
                 CHECK (data GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'),
    importo      REAL NOT NULL CHECK (importo > 0),           -- CHECK: importo > 0
    id_categoria INTEGER NOT NULL,
    descrizione  TEXT,                                        -- facoltativa
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria)   -- FOREIGN KEY
);

CREATE TABLE budget (
    id_budget    INTEGER PRIMARY KEY AUTOINCREMENT,           -- PRIMARY KEY
    mese         TEXT NOT NULL
                 CHECK (mese GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]'),
    id_categoria INTEGER NOT NULL,
    importo      REAL NOT NULL CHECK (importo > 0),           -- CHECK: budget > 0
    UNIQUE (mese, id_categoria),                              -- UNIQUE: un budget per mese/categoria
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria)   -- FOREIGN KEY
);

-- =====================================================
-- Dati di esempio
-- =====================================================

INSERT INTO categorie (nome) VALUES ('Alimentari'), ('Trasporti'), ('Svago');

INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES
    ('2025-01-15', 25.00,  1, 'Pranzo'),
    ('2025-01-20', 295.50, 1, 'Spesa mensile'),
    ('2025-01-22', 120.00, 2, 'Abbonamento mensile bus'),
    ('2025-02-03', 40.00,  3, 'Cinema e cena'),
    ('2025-02-10', 85.00,  1, 'Spesa settimanale');

INSERT INTO budget (mese, id_categoria, importo) VALUES
    ('2025-01', 1, 300.00),
    ('2025-01', 2, 150.00),
    ('2025-02', 3, 30.00);
