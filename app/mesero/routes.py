from flask import render_template, redirect, session, flash, url_for
from app.utils.db import get_db, log_audit
from app.utils.decorators import mesero_required
from app.mesero import bp


@bp.route('/pedidos')
@mesero_required
def mesero_pedidos():
    conn = get_db()
    cur = conn.execute('''
        SELECT pedidos.id, clientes.nombre as cliente, platos.nombre as plato,
               pedidos.cantidad, pedidos.estado, pedidos.fecha
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        JOIN platos ON pedidos.plato_id = platos.id
        ORDER BY pedidos.fecha DESC
    ''')
    pedidos = cur.fetchall()
    conn.close()
    return render_template('mesero/pedidos.html', pedidos=pedidos)


@bp.route('/pedidos/<int:pedido_id>/deliver')
@mesero_required
def mesero_deliver_pedido(pedido_id):
    conn = get_db()
    conn.execute("UPDATE pedidos SET estado = 'entregado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
    log_audit(session['user_id'], 'PEDIDO_DELIVERED', f'Pedido ID: {pedido_id}')
    flash('Pedido entregado', 'success')
    return redirect(url_for('mesero.mesero_pedidos'))


@bp.route('/pedidos/<int:pedido_id>/cancel')
@mesero_required
def mesero_cancel_pedido(pedido_id):
    conn = get_db()
    conn.execute("UPDATE pedidos SET estado = 'cancelado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
    log_audit(session['user_id'], 'PEDIDO_CANCELLED', f'Pedido ID: {pedido_id}')
    flash('Pedido cancelado', 'info')
    return redirect(url_for('mesero.mesero_pedidos'))