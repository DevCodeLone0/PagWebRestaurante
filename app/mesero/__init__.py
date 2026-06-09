from flask import Blueprint

bp = Blueprint('mesero', __name__, url_prefix='/mesero')

from app.mesero import routes  # noqa