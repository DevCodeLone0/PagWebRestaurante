from flask import render_template, request, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from app.utils.db import get_db, log_audit
from app.utils.decorators import login_required
from app.utils.validation import validate_password
from app.auth import bp


@bp.route('/')
def index():
    return redirect('/restaurante')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        ip_address = request.remote_addr

        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user:
            if user['locked_until']:
                locked_until = datetime.fromisoformat(user['locked_until'])
                if datetime.now() < locked_until:
                    remaining = (locked_until - datetime.now()).seconds // 60
                    flash(f'Cuenta bloqueada. Intenta en {remaining} minutos', 'error')
                    conn.close()
                    return render_template('login.html')
                else:
                    conn.execute('UPDATE users SET failed_attempts = 0, locked_until = NULL WHERE id = ?', (user['id'],))
                    conn.commit()

            if not user['is_active']:
                flash('Tu cuenta está desactivada. Contacta al administrador', 'error')
                conn.close()
                return render_template('login.html')

            if check_password_hash(user['password_hash'], password):
                conn.execute('UPDATE users SET last_login = ?, failed_attempts = 0, locked_until = NULL WHERE id = ?',
                             (datetime.now().isoformat(), user['id']))
                conn.commit()
                conn.close()

                session['user_id'] = user['id']
                session['email'] = user['email']
                session['rol'] = user['rol']
                session['last_activity'] = datetime.now().isoformat()

                log_audit(user['id'], 'LOGIN_SUCCESS', ip_address=ip_address)

                if user['must_change_password']:
                    flash('Debes cambiar tu contraseña antes de continuar', 'warning')
                    return redirect(url_for('auth.change_password'))

                flash('Has iniciado sesión correctamente', 'success')

                if user['rol'] == 'admin':
                    return redirect(url_for('admin.admin_users'))
                elif user['rol'] == 'chef':
                    return redirect(url_for('chef.chef_pedidos'))
                elif user['rol'] == 'mesero':
                    return redirect(url_for('mesero.mesero_pedidos'))
                else:
                    return redirect(url_for('main.restaurante'))
            else:
                failed_attempts = user['failed_attempts'] + 1
                locked_until = None

                if failed_attempts >= 5:
                    locked_until = (datetime.now() + timedelta(minutes=15)).isoformat()
                    flash('Demasiados intentos fallidos. Cuenta bloqueada por 15 minutos', 'error')
                else:
                    remaining = 5 - failed_attempts
                    flash(f'Credenciales incorrectas. Te quedan {remaining} intentos', 'error')

                conn.execute('UPDATE users SET failed_attempts = ?, locked_until = ? WHERE id = ?',
                             (failed_attempts, locked_until, user['id']))
                conn.commit()
                conn.close()

                log_audit(user['id'], 'LOGIN_FAILED', ip_address=ip_address)
                return render_template('login.html')
        else:
            conn.close()
            flash('Credenciales incorrectas', 'error')
            log_audit(None, 'LOGIN_FAILED_USER_NOT_FOUND', ip_address=ip_address)
            return render_template('login.html')

    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        ip_address = request.remote_addr

        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html')

        valid, msg = validate_password(password)
        if not valid:
            flash(msg, 'error')
            return render_template('register.html')

        conn = get_db()

        existing = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing:
            flash('El email ya está registrado', 'error')
            conn.close()
            return render_template('register.html')

        password_hash = generate_password_hash(password)

        try:
            conn.execute(
                'INSERT INTO users (email, password_hash, rol, created_at) VALUES (?, ?, ?, ?)',
                (email, password_hash, 'cliente', datetime.now().isoformat())
            )
            conn.commit()

            user_id = conn.execute('SELECT last_insert_rowid()').fetchone()[0]

            cliente_id = conn.execute(
                'INSERT INTO clientes (nombre, telefono, direccion, user_id) VALUES (?, ?, ?, ?)',
                (nombre, telefono, direccion, user_id)
            ).lastrowid
            conn.commit()

            log_audit(user_id, 'REGISTER', f'Cliente ID: {cliente_id}', ip_address)
            conn.close()

            flash('Registro exitoso. Ahora puedes iniciar sesión', 'success')
            return redirect(url_for('auth.login'))
        except Exception:
            conn.rollback()
            flash('Error al registrar. Intenta nuevamente', 'error')
            conn.close()
            return render_template('register.html')

    return render_template('register.html')


@bp.route('/logout')
@login_required
def logout():
    if 'user_id' in session:
        log_audit(session['user_id'], 'LOGOUT', ip_address=request.remote_addr)
    session.clear()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('auth.login'))


@bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        conn = get_db()
        user = conn.execute('SELECT password_hash FROM users WHERE id = ?', (session['user_id'],)).fetchone()

        if not check_password_hash(user['password_hash'], current_password):
            flash('La contraseña actual es incorrecta', 'error')
            conn.close()
            return render_template('change_password.html')

        if new_password != confirm_password:
            flash('Las nuevas contraseñas no coinciden', 'error')
            conn.close()
            return render_template('change_password.html')

        valid, msg = validate_password(new_password)
        if not valid:
            flash(msg, 'error')
            conn.close()
            return render_template('change_password.html')

        password_hash = generate_password_hash(new_password)
        conn.execute('UPDATE users SET password_hash = ?, must_change_password = 0 WHERE id = ?',
                     (password_hash, session['user_id']))
        conn.commit()
        conn.close()

        log_audit(session['user_id'], 'PASSWORD_CHANGE')
        flash('Contraseña actualizada correctamente', 'success')

        if session['rol'] == 'admin':
            return redirect(url_for('admin.admin_users'))
        elif session['rol'] == 'chef':
            return redirect(url_for('chef.chef_pedidos'))
        elif session['rol'] == 'mesero':
            return redirect(url_for('mesero.mesero_pedidos'))
        else:
            return redirect(url_for('main.restaurante'))

    return render_template('change_password.html')