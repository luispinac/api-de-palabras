import sqlite3

conn = sqlite3.connect("palabras.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE palabras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        palabra TEXT NOT NULL,
        categoria TEXT NOT NULL
    )
""")

datos = [
    ("gato", "animales"),
    ("pantalla", "tecnologia"),
    ("alegría", "emociones"),
    ("perro", "animales"),
    ("ratón", "tecnologia"),
    ("tristeza", "emociones"),
]

cursor.executemany("INSERT INTO palabras (palabra, categoria) VALUES (?, ?)", datos)

conn.commit()
conn.close()
