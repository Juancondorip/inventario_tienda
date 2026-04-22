from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'inventario.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre    TEXT NOT NULL,
            categoria TEXT NOT NULL,
            precio    REAL NOT NULL,
            stock     INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# ── LISTAR (ruta principal) ───────────────────────────────────────────────────
@app.route('/')
def listar():
    conn = get_db()
    productos = conn.execute('SELECT * FROM productos ORDER BY id').fetchall()
    conn.close()
    return render_template('listar.html', productos=productos)


# ── REGISTRAR ─────────────────────────────────────────────────────────────────
@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        nombre    = request.form['nombre']
        categoria = request.form['categoria']
        precio    = request.form['precio']
        stock     = request.form['stock']
        conn = get_db()
        conn.execute(
            'INSERT INTO productos (nombre, categoria, precio, stock) VALUES (?, ?, ?, ?)',
            (nombre, categoria, precio, stock)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))
    return render_template('registrar.html')


# ── EDITAR ────────────────────────────────────────────────────────────────────
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = get_db()
    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        nombre    = request.form['nombre']
        categoria = request.form['categoria']
        precio    = request.form['precio']
        stock     = request.form['stock']
        conn.execute(
            'UPDATE productos SET nombre=?, categoria=?, precio=?, stock=? WHERE id=?',
            (nombre, categoria, precio, stock, id)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('listar'))
    conn.close()
    return render_template('editar.html', producto=producto)


# ── ELIMINAR ──────────────────────────────────────────────────────────────────
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    conn = get_db()
    conn.execute('DELETE FROM productos WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('listar'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
