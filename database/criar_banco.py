import sqlite3

conn = sqlite3.connect("database/iim.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS maquinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT,
    nome TEXT,
    fabricante TEXT,
    modelo TEXT
)

""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS manutencoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maquina_id INTEGER,
    data_manutencao TEXT,
    falha TEXT,
    diagnostico TEXT,
    solucao TEXT,
    tecnico TEXT,
    tempo_parada INTEGER,
    FOREIGN KEY(maquina_id) REFERENCES maquinas(id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS falhas_conhecidas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sintoma TEXT,
    causa TEXT,
    solucao TEXT,
    incidencias INTEGER DEFAULT 0
)
""")


conn.commit()
conn.close()

print("Banco criado com sucesso!")
