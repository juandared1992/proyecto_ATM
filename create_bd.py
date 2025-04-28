import sqlite3
conn = sqlite3.connect("atm.db")
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS cuentas (
id INTEGER PRIMARY KEY AUTOINCREMENT,
numero_cuenta TEXT UNIQUE NOT NULL,
pin TEXT NOT NULL,
saldo REAL DEFAULT 0.0
)
''')
cursor.execute('''

INSERT OR IGNORE INTO cuentas (numero_cuenta, pin, saldo)
VALUES (?, ?, ?)
''', ("123456", "7890", 1000.0))
conn.commit()
conn.close()
print(" Base de datos 'atm.db' creada con éxito con una cuenta de prueba.")
