from flask import render_template, request, redirect, session, flash, url_for
from datetime import datetime

from app.utils.db import get_db, log_audit
from app.utils.decorators import login_required, admin_required, mesero_required
from app.main import bp


@bp.route('/restaurante')
@login_required
def restaurante():
    conn = get_db()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    entradas = conn.execute("SELECT * FROM platos WHERE categoria = 'entradas'").fetchall()
    platos_fuertes = conn.execute("SELECT * FROM platos WHERE categoria = 'platos_fuertes'").fetchall()
    postres = conn.execute("SELECT * FROM platos WHERE categoria = 'postres'").fetchall()
    conn.close()
    return render_template('restaurante.html', clientes=clientes, entradas=entradas, platos_fuertes=platos_fuertes, postres=postres)


@bp.route('/ordenar', methods=['POST'])
@login_required
def ordenar():
    cliente_id = request.form['cliente_id']
    plato_id = request.form['plato_id']
    cantidad = request.form['cantidad']
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = get_db()
    conn.execute('INSERT INTO pedidos (cliente_id, plato_id, cantidad, fecha) VALUES (?, ?, ?, ?)',
                 (cliente_id, plato_id, cantidad, fecha))
    conn.commit()
    conn.close()

    flash('Pedido realizado con éxito', 'success')
    return redirect('/pedidos')


@bp.route('/pedidos')
@login_required
def pedidos():
    conn = get_db()
    if session['rol'] == 'cliente':
        cliente = conn.execute('SELECT id FROM clientes WHERE user_id = ?', (session['user_id'],)).fetchone()
        if cliente:
            cur = conn.execute('''
                SELECT pedidos.id, clientes.nombre as cliente, platos.nombre as plato,
                       pedidos.cantidad, pedidos.estado, pedidos.fecha
                FROM pedidos
                JOIN clientes ON pedidos.cliente_id = clientes.id
                JOIN platos ON pedidos.plato_id = platos.id
                WHERE pedidos.cliente_id = ?
            ''', (cliente['id'],))
        else:
            cur = None
    else:
        cur = conn.execute('''
            SELECT pedidos.id, clientes.nombre as cliente, platos.nombre as plato,
                   pedidos.cantidad, pedidos.estado, pedidos.fecha
            FROM pedidos
            JOIN clientes ON pedidos.cliente_id = clientes.id
            JOIN platos ON pedidos.plato_id = platos.id
        ''')

    pedidos = cur.fetchall() if cur else []
    conn.close()
    return render_template('pedidos.html', pedidos=pedidos)


@bp.route('/proveedores')
@admin_required
def proveedores():
    return render_template('proveedores.html')


@bp.route('/registrar_proveedor', methods=['POST'])
@admin_required
def registrar_proveedor():
    nombre = request.form['nombre']
    empresa = request.form['empresa']
    telefono = request.form['telefono']
    email = request.form['email']
    producto = request.form['producto']

    conn = get_db()
    conn.execute('INSERT INTO proveedores (nombre, empresa, telefono, email, producto) VALUES (?, ?, ?, ?, ?)',
                 (nombre, empresa, telefono, email, producto))
    conn.commit()
    conn.close()

    flash('Proveedor registrado', 'success')
    return redirect('/proveedores')


@bp.route('/ver_proveedores')
@admin_required
def ver_proveedores():
    conn = get_db()
    proveedores = conn.execute('SELECT * FROM proveedores').fetchall()
    conn.close()
    return render_template('ver_proveedores.html', proveedores=proveedores)


@bp.route('/clientes')
@mesero_required
def clientes():
    return render_template('clientes.html')


@bp.route('/registrar_cliente', methods=['POST'])
@mesero_required
def registrar_cliente():
    nombre = request.form['nombre']
    telefono = request.form['telefono']
    direccion = request.form['direccion']

    conn = get_db()
    conn.execute('INSERT INTO clientes (nombre, telefono, direccion) VALUES (?, ?, ?)',
                 (nombre, telefono, direccion))
    conn.commit()
    conn.close()

    flash('Cliente registrado', 'success')
    return redirect('/clientes')


@bp.route('/ver_clientes')
@mesero_required
def ver_clientes():
    conn = get_db()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('ver_clientes.html', clientes=clientes)


@bp.route('/platos')
@admin_required
def platos():
    return render_template('platos.html')


@bp.route('/registrar_plato', methods=['POST'])
@admin_required
def registrar_plato():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    categoria = request.form['categoria']

    conn = get_db()
    conn.execute('INSERT INTO platos (nombre, descripcion, precio, categoria) VALUES (?, ?, ?, ?)',
                 (nombre, descripcion, precio, categoria))
    conn.commit()
    conn.close()

    flash('Plato registrado', 'success')
    return redirect('/platos')


@bp.route('/hacer_pedido')
@mesero_required
def hacer_pedido():
    conn = get_db()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    entradas = conn.execute("SELECT * FROM platos WHERE categoria = 'entradas'").fetchall()
    platos_fuertes = conn.execute("SELECT * FROM platos WHERE categoria = 'platos_fuertes'").fetchall()
    postres = conn.execute("SELECT * FROM platos WHERE categoria = 'postres'").fetchall()
    conn.close()
    return render_template('hacer_pedido.html', clientes=clientes, entradas=entradas,
                           platos_fuertes=platos_fuertes, postres=postres)