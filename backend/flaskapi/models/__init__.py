from werkzeug.local import LocalProxy
from flask_jwt_extended import get_current_user
from extensions import jwt_manager
from .manager import Manager
from .enterprise import Enterprise

@jwt_manager.user_lookup_loader
def lookup_manager(header: dict, data: dict):
    return Manager.find_by_id(data.get('sub'))

current_manager: Manager = LocalProxy(get_current_user)
