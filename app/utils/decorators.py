from functools import wraps
from datetime import datetime, timedelta
from flask import session, flash, redirect, url_for, request


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('auth.login'))

        if 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(minutes=30):
                session.clear()
                flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente', 'warning')
                return redirect(url_for('auth.login'))

        session['last_activity'] = datetime.now().isoformat()
        return f(*args, **kwargs)
    return decorated_function


def role_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('auth.login'))

            if session.get('rol') not in roles:
                flash('No tienes permisos para acceder a esta página', 'error')
                return redirect(url_for('main.index'))

            if 'last_activity' in session:
                last_activity = datetime.fromisoformat(session['last_activity'])
                if datetime.now() - last_activity > timedelta(minutes=30):
                    session.clear()
                    flash('Tu sesión ha expirado. Por favor, inicia sesión nuevamente', 'warning')
                    return redirect(url_for('auth.login'))

            session['last_activity'] = datetime.now().isoformat()
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return role_required('admin')(f)


def chef_required(f):
    return role_required('admin', 'chef')(f)


def mesero_required(f):
    return role_required('admin', 'mesero')(f)