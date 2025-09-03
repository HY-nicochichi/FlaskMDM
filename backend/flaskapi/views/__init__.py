from .view_doc import bp_doc
from .view_manager import bp_manager
from .view_enterprise import bp_enterprise
from models import Manager
from extensions import jwt_manager

bps = [
    bp_doc,
    bp_manager,
    bp_enterprise
]

@jwt_manager.user_lookup_loader
def lookup_user(header, data):
    return Manager.query.filter_by(id=data['sub']).one_or_none()
