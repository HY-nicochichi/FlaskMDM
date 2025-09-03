import {getJwt} from '~/composables/JwtManager'
import type {Resp} from '~/types'

function getOptions(): RequestInit {
  return {
    method: 'GET',
    mode: 'cors',
    headers: {
      'Authorization': 'Bearer ' + getJwt()
    }
  }
}

function postOptions(json: any): RequestInit {
  return {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getJwt()
    },
    body: JSON.stringify(json)
  }
}

function patchOptions(json: any): RequestInit {
  return {
    method: 'PATCH',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getJwt()
    },
    body: JSON.stringify(json)
  }
}

function deleteOptions(): RequestInit {
  return {
    method: 'DELETE',
    mode: 'cors',
    headers: {
      'Authorization': 'Bearer ' + getJwt()
    }
  }
}

async function apiRequest(
  route: string = '/',
  options: RequestInit = getOptions()
): Promise<Resp> {
  try {
    const response: Response = await fetch(
      useRuntimeConfig().public.apiUrlBase + route, options
    )
    return {
      status: response.status,
      json: await response.json()
    }
  }
  catch(error) {
    return {
      status: 500,
      json: {'msg': 'API access failed'}
    }
  }
}

async function accessManagerPost(
  id: string, password: string
): Promise<Resp> {
  return apiRequest(
    '/manager/', postOptions({
      id: id,
      password: password
    })
  )
}

async function accessManagerGet(): Promise<Resp> {
  return apiRequest(
    '/manager/', getOptions()
  )
}

async function accessManagerDelete(): Promise<Resp> {
  return apiRequest(
    '/manager/', deleteOptions()
  )
}

async function accessManagerAccessTokenPost(
  id: string, password: string
): Promise<Resp> {
  return apiRequest(
    '/manager/access_token', postOptions({
      id: id,
      password: password
    })
  )
}

async function accessManagerGoogleSignupGet(): Promise<Resp> {
  return apiRequest(
    '/manager/google_signup', getOptions()
  )
}

async function accessEnterprisePost(
  signup_url_name: string, enterprise_token: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/', postOptions({
      signup_url_name: signup_url_name,
      enterprise_token: enterprise_token
    })
  )
}

async function accessEnterpriseGet(
  enterprise_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id, getOptions()
  )
}

async function accessEnterpriseDelete(
  enterprise_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id, deleteOptions()
  )
}

async function accessDevicePatch(
  enterprise_id: string, device_id: string, policy_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id + '/device/' + device_id,
    patchOptions({policy_id: policy_id})
  )
}

async function accessDeviceDelete(
  enterprise_id: string, device_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id + '/device/' + device_id,
    deleteOptions()
  )
}

async function accessPolicyGet(
  enterprise_id: string, policy_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id + '/policy/' + policy_id,
    getOptions()
  )
}

async function accessPolicyPatch(
  enterprise_id: string, policy_id: string, policy: any
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id + '/policy/' + policy_id,
    patchOptions({policy: policy})
  )
}

async function accessPolicyDelete(
  enterprise_id: string, policy_id: string
): Promise<Resp> {
  return apiRequest(
    '/enterprise/' + enterprise_id + '/policy/' + policy_id,
    deleteOptions()
  )
}

export {
  accessManagerPost, accessManagerGet, accessManagerDelete,
  accessManagerAccessTokenPost, accessManagerGoogleSignupGet,
  accessEnterprisePost, accessEnterpriseGet, accessEnterpriseDelete,
  accessDevicePatch, accessDeviceDelete,
  accessPolicyGet, accessPolicyPatch, accessPolicyDelete
}
