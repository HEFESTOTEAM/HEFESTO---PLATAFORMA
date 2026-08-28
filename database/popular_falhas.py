import sqlite3

conn = sqlite3.connect("database/iim.db")
cursor = conn.cursor()

falhas = [

    (
        "motor não liga",
        "Contator queimado",
        "Substituir contator",
        12
    ),

    (
        "motor não liga",
        "Relé térmico desarmado",
        "Rearmar relé",
        8
    ),

    (
        "sensor falhando",
        "Sensor desalinhado",
        "Realizar ajuste",
        15
    ),

    (
        "servo não habilita",
        "Encoder com falha",
        "Verificar cabo encoder",
        6
    )

]

cursor.executemany("""
INSERT INTO falhas_conhecidas
(
    sintoma,
    causa,
    solucao,
    incidencias
)
VALUES (?, ?, ?, ?)
""", falhas)



conn.commit()
conn.close()

print("Falhas cadastradas")