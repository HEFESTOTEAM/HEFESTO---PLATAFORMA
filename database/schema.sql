CREATE TABLE maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    fabricante TEXT,
    modelo TEXT,
    numero_serie TEXT,
    setor TEXT,
    linha TEXT,
    plc TEXT,
    ihm TEXT,
    criticidade TEXT,
    status TEXT
);
CREATE TABLE maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    fabricante TEXT,
    modelo TEXT,
    numero_serie TEXT,
    setor TEXT,
    linha TEXT,
    plc TEXT,
    ihm TEXT,
    criticidade TEXT,
    status TEXT
);CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    login TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL,
    nivel TEXT NOT NULL
);

CREATE TABLE maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT NOT NULL,
    nome TEXT NOT NULL,
    fabricante TEXT,
    modelo TEXT,
    numero_serie TEXT,
    plc TEXT,
    ihm TEXT,
    setor TEXT,
    linha TEXT,
    criticidade TEXT,
    status TEXT
);

CREATE TABLE manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maquina_id INTEGER,
    data_manutencao TEXT,
    falha TEXT,
    diagnostico TEXT,
    solucao TEXT,
    tecnico TEXT,
    tempo_parada INTEGER,
    FOREIGN KEY(maquina_id) REFERENCES maquinas(id)
);
