from flask import render_template, redirect, session, flash, url_for
from app.utils.db import get_db, log_audit
from app.utils.decorators import chef_required
from app.chef import bp


@bp.route('/pedidos')
@chef_required
def chef_pedidos():
    conn = get_db()
    cur = conn.execute('''
        SELECT pedidos.id, clientes.nombre as cliente, platos.nombre as plato,
               pedidos.cantidad, pedidos.estado, pedidos.fecha
        FROM pedidos
        JOIN clientes ON pedidos.cliente_id = clientes.id
        JOIN platos ON pedidos.plato_id = platos.id
        WHERE pedidos.estado = 'pendiente' OR pedidos.estado = 'en_preparacion'
        ORDER BY pedidos.fecha ASC
    ''')
    pedidos = cur.fetchall()
    conn.close()
    return render_template('chef/pedidos.html', pedidos=pedidos)


@bp.route('/pedidos/<int:pedido_id>/start')
@chef_required
def chef_start_pedido(pedido_id):
    conn = get_db()
    conn.execute("UPDATE pedidos SET estado = 'en_preparacion' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
    log_audit(session['user_id'], 'PEDIDO_START', f'Pedido ID: {pedido_id}')
    flash('Pedido en preparación', 'info')
    return redirect(url_for('chef.chef_pedidos'))


@bp.route('/pedidos/<int:pedido_id>/complete')
@chef_required
def chef_complete_pedido(pedido_id):
    conn = get_db()
    conn.execute("UPDATE pedidos SET estado = 'listo' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
    log_audit(session['user_id'], 'PEDIDO_COMPLETE', f'Pedido ID: {pedido_id}')
    flash('Pedido marcado como listo', 'success')
    return redirect(url_for('chef.chef_pedidos'))