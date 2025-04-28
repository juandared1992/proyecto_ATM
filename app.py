from flask import Flask, render_template, request, redirect, session
import sqlite3
from waitress import serve

app = Flask(__name__)
app.secret_key = 'secreto123'

def obtener_cuenta(numero_cuenta):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cuentas WHERE numero_cuenta = ?", (numero_cuenta,))
    cuenta = cursor.fetchone()
    conn.close()
    return cuenta

def actualizar_saldo(numero_cuenta, nuevo_saldo):
    conn = sqlite3.connect("atm.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE cuentas SET saldo = ? WHERE numero_cuenta = ?", (nuevo_saldo, numero_cuenta))
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        numero = request.form['numero']
        pin = request.form['pin']
        cuenta = obtener_cuenta(numero)
        if cuenta and str(cuenta[2]) == pin:  
            session['numero_cuenta'] = numero
            return redirect('/dashboard')
        else:
            return render_template('mensaje.html', mensaje="Credenciales incorrectas.")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'numero_cuenta' not in session:
        return redirect('/')
    cuenta = obtener_cuenta(session['numero_cuenta'])
    return render_template('dashboard.html', cuenta=cuenta)

@app.route('/retirar', methods=['POST'])
def retirar():
    if 'numero_cuenta' not in session:
        return redirect('/')
    monto = float(request.form['monto'])
    cuenta = obtener_cuenta(session['numero_cuenta'])
    if not cuenta:
        return render_template('mensaje.html', mensaje="Cuenta no encontrada.")
    if monto > cuenta[3]:
        return render_template('mensaje.html', mensaje="Saldo insuficiente.")
    nuevo_saldo = cuenta[3] - monto
    actualizar_saldo(cuenta[1], nuevo_saldo)
    return render_template('mensaje.html', mensaje=f"Retiro exitoso. Nuevo saldo: ${nuevo_saldo:.2f}")

@app.route('/depositar', methods=['POST'])
def depositar():
    if 'numero_cuenta' not in session:
        return redirect('/')
    monto = float(request.form['monto'])
    cuenta = obtener_cuenta(session['numero_cuenta'])
    if not cuenta:
        return render_template('mensaje.html', mensaje="Cuenta no encontrada.")
    nuevo_saldo = cuenta[3] + monto
    actualizar_saldo(cuenta[1], nuevo_saldo)
    return render_template('mensaje.html', mensaje=f"Depósito exitoso. Nuevo saldo: ${nuevo_saldo:.2f}")

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':  
    serve(app, host='0.0.0.0', port=8080)