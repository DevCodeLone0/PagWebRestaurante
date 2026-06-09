import os
from flask import Flask, session
from datetime import datetime, timedelta
from app.config import config
from app.utils.db import init_db, close_db


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    # Point to project root for static/ and templates/
    root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    app = Flask(__name__, instance_relative_config=False, root_path=root_path)
    app.config.from_object(config[config_name])

    # Session timeout check before every request
    @app.before_request
    def check_session_timeout():
        if 'user_id' in session and 'last_activity' in session:
            last_activity = datetime.fromisoformat(session['last_activity'])
            if datetime.now() - last_activity > timedelta(minutes=app.config['SESSION_TIMEOUT']):
                session.clear()

    # Current user available in all templates
    @app.context_processor
    def inject_user():
        if 'user_id' in session:
            from app.utils.db import get_db
            conn = get_db()
            user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
            conn.close()
            return dict(current_user=user)
        return dict(current_user=None)

    # Initialize database
    with app.app_context():
        init_db()

    # Register teardown
    app.teardown_appcontext(close_db)

    # Register blueprints
    from app.auth import bp as auth_bp
    from app.main import bp as main_bp
    from app.admin import bp as admin_bp
    from app.chef import bp as chef_bp
    from app.mesero import bp as mesero_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chef_bp)
    app.register_blueprint(mesero_bp)

    return app