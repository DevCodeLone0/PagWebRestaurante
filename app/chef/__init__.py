from flask import Blueprint

bp = Blueprint('chef', __name__, url_prefix='/chef')

from app.chef import routes  # noqa