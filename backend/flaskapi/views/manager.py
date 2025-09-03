from flask import (
    Blueprint,
    request,
    current_app
)
from flask_jwt_extended import (
    jwt_required,
    create_access_token
)
from models import (
    current_manager,
    Manager
)
from extensions import (
    db_transaction,
    amapi_client
)

bp_manager = Blueprint('bp_manager', __name__, url_prefix='/manager')

@bp_manager.post('/')
def create_manager() -> tuple[dict, int]:
    with db_transaction():
        manager = Manager.create(request.json['id'], request.json['password'])
    if manager:
        return {'msg': '成功'}, 200
    else:
        return {'msg': 'マネージャーIDが既に存在します'}, 409

@bp_manager.get('/')
@jwt_required()
def get_manager() -> tuple[dict, int]:
    enterprises: list[dict] = []
    for enterprise in current_manager.enterprises:
        enterprise_info: dict = amapi_client.enterprises().get(
            name = f'enterprises/{enterprise.id}'
        ).execute()
        enterprises.append({
            'id': enterprise_info.get('name', '組織IDなし').split('/')[-1],
            'name': enterprise_info.get('enterpriseDisplayName', '組織名なし')
        })
    return {'id': current_manager.id, 'enterprises': enterprises}, 200

@bp_manager.delete('/')
@jwt_required()
def delete_manager() -> tuple[dict, int]:
    for enterprise in current_manager.enterprises:
        amapi_client.enterprises().delete(
            name = f'enterprises/{enterprise.id}'
        ).execute()
    with db_transaction():
        current_manager.delete()
    return {'msg': '成功'}, 200

@bp_manager.post('/access_token')
def access_token() -> tuple[dict, int]:
    manager: Manager|None = Manager.find_by_id(request.json['id'])
    if manager and manager.is_password_matched(request.json['password']):
        return {'access_token': create_access_token(request.json['id'])}, 200
    else:
        return {'msg': 'マネージャーIDかパスワードが誤っています'}, 401

@bp_manager.get('/google_signup')
@jwt_required()
def google_signup() -> tuple[dict, int]:
    signup: dict = amapi_client.signupUrls().create(
        projectId = current_app.config['GOOGLE_CLOUD_PROJECT_ID'],
        callbackUrl = 'https://storage.googleapis.com/android-management-quick-start/enterprise_signup_callback.html'
    ).execute()
    return {'google_signup': {'url': signup['url'], 'name': signup['name']}}, 200
