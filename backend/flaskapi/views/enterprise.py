from flask import (
    Blueprint,
    request,
    current_app
)
from flask_jwt_extended import jwt_required
from models import (
    current_manager,
    Enterprise
)
from extensions import (
    db_transaction,
    amapi_client
)

bp_enterprise = Blueprint('bp_enterprise', __name__, url_prefix='/enterprise')

@bp_enterprise.post('/')
@jwt_required()
def create_enterprise() -> tuple[dict, int]:
    enterprise: dict = amapi_client.enterprises().create(
        projectId = current_app.config['GOOGLE_CLOUD_PROJECT_ID'],
        signupUrlName = request.json['signup_url_name'],
        enterpriseToken = request.json['enterprise_token'],
        body = {}
    ).execute()
    id: str = enterprise['name'].split('/')[-1]
    amapi_client.enterprises().policies().patch(
        name = f'enterprises/{id}/policies/default',
        body = {
            'applications': [
                {
                    'packageName': 'com.android.chrome',
                    'installType': 'FORCE_INSTALLED'
                }
            ]
        }
    ).execute()
    enroll_qrcode: str = amapi_client.enterprises().enrollmentTokens().create(
        parent = f'enterprises/{id}',
        body = {
            'duration': '315576000s',
            'policyName': f'enterprises/{id}/policies/default'
        }
    ).execute()['qrCode']
    with db_transaction():
        Enterprise.create(
            id=id, enroll_qrcode=enroll_qrcode, manager_id=current_manager.id
        )
    return {'msg': '成功'}, 200

@bp_enterprise.get('/<id>')
@jwt_required()
def get_enterprise(id: str) -> tuple[dict, int]:
    name: str = amapi_client.enterprises().get(
        name = f'enterprises/{id}'
    ).execute().get('enterpriseDisplayName', '組織名なし')
    devices_res: dict = amapi_client.enterprises().devices().list(
        parent = 'enterprises/' + id
    ).execute()
    devices: list[dict] = [
        {
            'id': device.get('name', 'デバイスIDなし').split('/')[-1],
            'model': device.get('hardwareInfo', {}).get('model', 'モデル名なし'),
            'serial_number': device.get('hardwareInfo', {}).get('serialNumber', 'シリアル番号なし'),
            'policy': device.get('policyName', 'default').split('/')[-1]
        } for device in devices_res.get('devices', [])
    ]
    policies_res: dict = amapi_client.enterprises().policies().list(
        parent = 'enterprises/' + id
    ).execute()
    policies: list[str] = [
        policy['name'].split('/')[-1]
        for policy in policies_res.get('policies', [])
        if policy['name'].split('/')[-1] != 'default'
    ]
    return {
        'name': name,
        'enroll_qrcode': Enterprise.find_by_id(id).enroll_qrcode,
        'devices': devices, 
        'policies': policies
    }, 200

@bp_enterprise.delete('/<id>')
@jwt_required()
def delete_enterprise(id: str) -> tuple[dict, int]:
    amapi_client.enterprises().delete(
        name = f'enterprises/{id}'
    ).execute()
    with db_transaction():
        Enterprise.find_by_id(id).delete()
    return {'msg': '成功'}, 200

@bp_enterprise.patch('/<enterprise_id>/policy/<id>')
@jwt_required()
def patch_policy(id: str, enterprise_id: str) -> tuple[dict, int]:
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
def get_policy(enterprise_id: str, id: str) -> tuple[dict, int]:
    policy: dict = amapi_client.enterprises().policies().get(
        name = f'enterprises/{enterprise_id}/policies/{id}'
    ).execute()
    return {'policy': policy}, 200

@bp_enterprise.delete('/<enterprise_id>/policy/<id>')
@jwt_required()
def delete_policy(enterprise_id: str, id: str) -> tuple[dict, int]:
    amapi_client.enterprises().policies().delete(
        name = f'enterprises/{enterprise_id}/policies/{id}'
    ).execute()
    return {'msg': '成功'}, 200

@bp_enterprise.patch('/<enterprise_id>/device/<id>')
@jwt_required()
def patch_device(id: str, enterprise_id: str) -> tuple[dict, int]:
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
def delete_device(enterprise_id: str, id: str) -> tuple[dict, int]:
    amapi_client.enterprises().devices().delete(
        name = f'enterprises/{enterprise_id}/devices/{id}'
    ).execute()
    return {'msg': '成功'}, 200
