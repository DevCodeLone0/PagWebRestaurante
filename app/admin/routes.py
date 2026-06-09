from flask import render_template, request, redirect, session, flash, url_for
from datetime import datetime
from werkzeug.security import generate_password_hash

from app.utils.db import get_db, log_audit
from app.utils.decorators import admin_required
from app.utils.validation import validate_password
from app.admin import bp


@bp.route('/users')
@admin_required
def admin_users():
    conn = get_db()
    users = conn.execute('''
        SELECT users.*, clientes.nombre as cliente_nombre
        FROM users
        LEFT JOIN clientes ON users.id = clientes.user_id
        ORDER BY users.created_at DESC
    ''').fetchall()
    conn.close()
    return render_template('admin/users.html', users=users)


@bp.route('/users/create', methods=['GET', 'POST'])
@admin_required
def admin_create_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        rol = request.form['rol']

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('admin/create_user.html')

        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('admin/create_user.html')

        conn = get_db()

        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('El email ya está registrado', 'error')
            conn.close()
            return render_template('admin/create_user.html')

        password_hash = generate_password_hash(password)

        try:
            conn.execute(
                'INSERT INTO users (email, password_hash, rol, created_at) VALUES (?, ?, ?, ?)',
                (email, password_hash, rol, datetime.now().isoformat())
            )
            conn.commit()
            user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            log_audit(session['user_id'], 'USER_CREATED', f'User ID: {user_id}, Rol: {rol}')
            conn.close()

            flash(f'Usuario {rol} creado exitosamente', 'success')
            return redirect(url_for('admin.admin_users'))
        except Exception:
            conn.rollback()
            flash('Error al crear usuario', 'error')
            conn.close()
            return render_template('admin/create_user.html')

    return render_template('admin/create_user.html')


@bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def admin_toggle_user(user_id):
    if user_id == session['user_id']:
        flash('No puedes desactivar tu propia cuenta', 'error')
        return redirect(url_for('admin.admin_users'))

    conn = get_db()
    user = conn.execute('SELECT is_active, email, rol FROM users WHERE id = ?', (user_id,)).fetchone()

    if not user:
        flash('Usuario no encontrado', 'error')
        conn.close()
        return redirect(url_for('admin.admin_users'))

    new_state = 0 if user['is_active'] else 1
    conn.execute('UPDATE users SET is_active = ? WHERE id = ?', (new_state, user_id))
    conn.commit()
    conn.close()

    action = 'USER_ACTIVATED' if new_state else 'USER_DEACTIVATED'
    log_audit(session['user_id'], action, f'User ID: {user_id}')

    state_text = 'activada' if new_state else 'desactivada'
    flash(f'Usuario {state_text}', 'success')
    return redirect(url_for('admin.admin_users'))


@bp.route('/audit-log')
@admin_required
def ver_audit_log():
    conn = get_db()
    logs = conn.execute('''
        SELECT audit_log.*, users.email as user_email
        FROM audit_log
        LEFT JOIN users ON audit_log.user_id = users.id
        ORDER BY audit_log.timestamp DESC
        LIMIT 100
    ''').fetchall()
    conn.close()
    return render_template('admin/audit_log.html', logs=logs)