from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask import (
    Blueprint,
    request,
    current_app
)
from flask_jwt_extended import (
    jwt_required,
    current_user,
    create_access_token
)
from models import (
    Manager,
    Enterprise
)
from extensions import (
    amapi_client,
    db_orm
)

bp_manager = Blueprint('bp_manager', __name__, url_prefix='/manager')

@bp_manager.post('/')
def create_manager():
    if Manager.query.filter_by(id=request.json['id']).one_or_none():
        return {'msg': 'マネージャーIDが既に存在します'}, 409
    else:
        db_orm.session.add(
            Manager(
                id = request.json['id'],
                pass_enc = generate_password_hash(request.json['password'])
            )
        )
        db_orm.session.commit()
        return {'msg': '成功'}, 200

@bp_manager.get('/')
@jwt_required()
def get_manager():
    enterprises = []
    for enterprise in Enterprise.query.filter_by(manager_id=current_user.id).all():
        enterprise_info = amapi_client.enterprises().get(
            name = f'enterprises/{enterprise.id}'
        ).execute()
        enterprises.append({
            'id': enterprise_info.get('name', '組織IDなし').split('/')[-1],
            'name': enterprise_info.get('enterpriseDisplayName', '組織名なし')
        })
    return {'id': current_user.id, 'enterprises': enterprises}, 200

@bp_manager.delete('/')
@jwt_required()
def delete_manager():
    for enterprise in Enterprise.query.filter_by(manager_id=current_user.id).all():
        amapi_client.enterprises().delete(
            name = f'enterprises/{enterprise.id}'
        ).execute()
        db_orm.session.delete(enterprise)
    db_orm.session.delete(current_user)
    db_orm.session.commit()
    return {'msg': '成功'}, 200

@bp_manager.post('/access_token')
def create_token():
    manager = Manager.query.filter_by(id=request.json['id']).one_or_none()
    if manager == None:
        return {'msg': 'マネージャーIDが存在しません'}, 401
    elif check_password_hash(manager.pass_enc, request.json['password']) == False:
        return {'msg': 'パスワードが誤っています'}, 401
    else:
        return {'access_token': create_access_token(identity=request.json['id'])}, 200

@bp_manager.get('/google_signup')
@jwt_required()
def google_signup():
    signup = amapi_client.signupUrls().create(
        projectId = current_app.config['GOOGLE_CLOUD_PROJECT_ID'],
        callbackUrl = 'https://storage.googleapis.com/android-management-quick-start/enterprise_signup_callback.html'
    ).execute()
    return {'google_signup': {'url': signup['url'], 'name': signup['name']}}, 200
