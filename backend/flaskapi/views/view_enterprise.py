from flask import (
    Blueprint,
    request,
    current_app
)
from flask_jwt_extended import (
    jwt_required,
    current_user
)
from models import (
    Enterprise
)
from extensions import (
    amapi_client,
    db_orm
)

bp_enterprise = Blueprint('bp_enterprise', __name__, url_prefix='/enterprise')

@bp_enterprise.post('/')
@jwt_required()
def create_enterprise():
    enterprise = amapi_client.enterprises().create(
        projectId = current_app.config['GOOGLE_CLOUD_PROJECT_ID'],
        signupUrlName = request.json['signup_url_name'],
        enterpriseToken = request.json['enterprise_token'],
        body = {}
    ).execute()
    id = enterprise['name'].split('/')[-1]
    amapi_client.enterprises().policies().patch(
        name = f'enterprises/{id}/policies/default',
        body = {}
    ).execute()
    enroll_qrcode = amapi_client.enterprises().enrollmentTokens().create(
        parent = f'enterprises/{id}',
        body = {
            'duration': '315576000s',
            'policyName': f'enterprises/{id}/policies/default'
        }
    ).execute()['qrCode']
    db_orm.session.add(
        Enterprise(id=id, enroll_qrcode=enroll_qrcode, manager_id=current_user.id)
    )
    db_orm.session.commit()
    return {'msg': '成功'}, 200

@bp_enterprise.get('/<id>')
@jwt_required()
def get_enterprise(id: str):
    name = amapi_client.enterprises().get(
        name = f'enterprises/{id}'
    ).execute().get('enterpriseDisplayName', '組織名なし')
    devices_res = amapi_client.enterprises().devices().list(
        parent = 'enterprises/' + id
    ).execute()
    devices = [
        {
            'id': device.get('name', 'デバイスIDなし').split('/')[-1],
            'model': device.get('hardwareInfo', {}).get('model', 'モデル名なし'),
            'serial_number': device.get('hardwareInfo', {}).get('serialNumber', 'シリアル番号なし'),
            'policy': device.get('policyName', 'default').split('/')[-1]
        }
        for device in devices_res.get('devices', [])
    ]
    policies_res = amapi_client.enterprises().policies().list(
        parent = 'enterprises/' + id
    ).execute()
    policies = [
        policy['name'].split('/')[-1]
        for policy in policies_res.get('policies', [])
        if policy['name'].split('/')[-1] != 'default'
    ]
    return {
        'name': name,
        'enroll_qrcode': Enterprise.query.filter_by(id=id).one_or_none().enroll_qrcode, 
        'devices': devices, 
        'policies': policies
    }, 200

@bp_enterprise.delete('/<id>')
@jwt_required()
def delete_enterprise(id: str):
    amapi_client.enterprises().delete(
        name = f'enterprises/{id}'
    ).execute()
    db_orm.session.delete(Enterprise.query.filter_by(id=id).one_or_none())
    db_orm.session.commit()
    return {'msg': '成功'}, 200

@bp_enterprise.patch('/<enterprise_id>/policy/<id>')
@jwt_required()
def patch_policy(id: str, enterprise_id: str):
    if id == 'default':
        return {'msg': 'defaultはポリシーIDに指定できません'}, 400
    else:
        amapi_client.enterprises().policies().patch(
            name = f'enterprises/{enterprise_id}/policies/{id}',
            body = request.json['policy']
        ).execute()
        return {'msg': '成功'}, 200

@bp_enterprise.get('/<enterprise_id>/policy/<id>')
@jwt_required()
def get_policy(enterprise_id: str, id: str):
    policy = amapi_client.enterprises().policies().get(
        name = f'enterprises/{enterprise_id}/policies/{id}'
    ).execute()
    return {'policy': policy}, 200

@bp_enterprise.delete('/<enterprise_id>/policy/<id>')
@jwt_required()
def delete_policy(enterprise_id: str, id: str):
    amapi_client.enterprises().policies().delete(
        name = f'enterprises/{enterprise_id}/policies/{id}'
    ).execute()
    return {'msg': '成功'}, 200

@bp_enterprise.patch('/<enterprise_id>/device/<id>')
@jwt_required()
def patch_device(id: str, enterprise_id: str):
    amapi_client.enterprises().devices().patch(
        name = f'enterprises/{enterprise_id}/devices/{id}',
        updateMask = 'policyName',
        body = {
            'policyName': f'enterprises/{enterprise_id}/policies/{request.json['policy_id']}'
        }
    ).execute()
    return {'msg': '成功'}, 200

@bp_enterprise.delete('/<enterprise_id>/device/<id>')
@jwt_required()
def delete_device(enterprise_id: str, id: str):
    amapi_client.enterprises().devices().delete(
        name = f'enterprises/{enterprise_id}/devices/{id}'
    ).execute()
    return {'msg': '成功'}, 200
