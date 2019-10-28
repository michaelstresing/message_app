from main import app
from flask import Blueprint
from . import db
@bp.app_errorhandler(404)
