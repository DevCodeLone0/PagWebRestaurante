import sqlite3
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DB_PATH'])
        g.db.row_factory = sqlite3.Row
    else:
        # Verify connection is still open
        try:
            g.db.execute('SELECT 1')
        except sqlite3.ProgrammingError:
            g.db = sqlite3.connect(current_app.config['DB_PATH'])
            g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()

    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            rol TEXT NOT NULL DEFAULT 'cliente',
            created_at TEXT NOT NULL,
            last_login TEXT,
            is_active INTEGER DEFAULT 1,
            failed_attempts INTEGER DEFAULT 0,
            locked_until TEXT,
            must_change_password INTEGER DEFAULT 0
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            action TEXT NOT NULL,
            details TEXT,
            ip_address TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            direccion TEXT,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS platos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            categoria TEXT NOT NULL
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            plato_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            estado TEXT DEFAULT 'pendiente',
            fecha TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id),
            FOREIGN KEY (plato_id) REFERENCES platos (id)
        )
    ''')

    db.execute('''
        CREATE TABLE IF NOT EXISTS proveedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            empresa TEXT NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            producto TEXT NOT NULL
        )
    ''')

    db.commit()

    from werkzeug.security import generate_password_hash
    from datetime import datetime

    existing_admin = db.execute("SELECT id FROM users WHERE rol = 'admin'").fetchone()
    if not existing_admin:
        admin_hash = generate_password_hash('Admin1234')
        db.execute(
            'INSERT INTO users (email, password_hash, rol, created_at, must_change_password) VALUES (?, ?, ?, ?, ?)',
            ('admin@restaurante.com', admin_hash, 'admin', datetime.now().isoformat(), 1)
        )
        db.commit()


def log_audit(user_id, action, details=None, ip_address=None):
    from datetime import datetime
    db = get_db()
    db.execute(
        'INSERT INTO audit_log (user_id, action, details, ip_address, timestamp) VALUES (?, ?, ?, ?, ?)',
        (user_id, action, details, ip_address, datetime.now().isoformat())
    )
    db.commit()