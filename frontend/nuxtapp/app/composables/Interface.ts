interface Resp {
  status: number
  json: any
}

interface Alert {
  show: boolean
  msg: string
}

interface Manager {
  login: boolean
  id: string
  enterprises: {id: string, name: string}[]
}

interface Device {
  id: string
  model: string
  serial_number: string
  policy: string
}

interface Enterprise {
  name: string
  enroll_qrcode: string
  policies: string[]
  devices: Device[]
}

interface PasswordPolicy {
  passwordMinimumLength: number
  passwordQuality: 'NUMERIC'|'ALPHABETIC'|'ALPHANUMERIC'
  maximumFailedPasswordsForWipe: number
}

interface Policy {
  applications: {
    packageName: string
    installType: 'FORCE_INSTALLED'
  }[]
  passwordPolicies: PasswordPolicy[]
  cameraAccess: 'CAMERA_ACCESS_DISABLED'|'CAMERA_ACCESS_USER_CHOICE'
  systemUpdate: {
    type: 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'|'AUTOMATIC'
  },
  screenCaptureDisabled: boolean
  smsDisabled: boolean
  bluetoothDisabled: boolean
  factoryResetDisabled: boolean
}

export type {
  Resp, Alert, Manager, Enterprise, Device, PasswordPolicy, Policy
}
