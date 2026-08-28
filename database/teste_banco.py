import sqlite3

conn = sqlite3.connect("database/iim.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO manutencoes
(maquina_id, falha, diagnostico, solucao, tecnico)
VALUES (?, ?, ?, ?, ?)
""", (
    1,
    "Motor não liga",
    "Contator queimado",
    "Substituição do contator KM1",
    "Paulo Costa"
))


conn.commit()

cursor.execute("SELECT * FROM manutencoes")

print(cursor.fetchall())

conn.close()


