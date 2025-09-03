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

interface ApplicationPolicy {
  packageName: string
  installType: 'FORCE_INSTALLED'
  managedConfiguration?: {
    URLBlocklist: ['*'],
    URLAllowlist: string[]
  }
}

interface PasswordPolicy {
  passwordMinimumLength: number
  passwordQuality: 'NUMERIC'|'ALPHABETIC'|'ALPHANUMERIC'
  maximumFailedPasswordsForWipe: number
}

interface DeviceConnectionPolicy {
  usbDataAccess: 'DISALLOW_USB_FILE_TRANSFER'|'ALLOW_USB_DATA_TRANSFER'
  tetheringSettings: 'DISALLOW_ALL_TETHERING'|'ALLOW_ALL_TETHERING'
  wifiSsidPolicy: {
    wifiSsidPolicyType: 'WIFI_SSID_DENYLIST'|'WIFI_SSID_ALLOWLIST'
    wifiSsids: {
      wifiSsid: string
    }[]
  }
}

interface Policy {
  applications: ApplicationPolicy[]
  passwordPolicies: PasswordPolicy[]
  cameraAccess: 'CAMERA_ACCESS_DISABLED'|'CAMERA_ACCESS_USER_CHOICE'
  microphoneAccess: 'MICROPHONE_ACCESS_DISABLED'|'MICROPHONE_ACCESS_USER_CHOICE'
  systemUpdate: {
    type: 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'|'AUTOMATIC'
  }
  screenCaptureDisabled: boolean
  smsDisabled: boolean
  bluetoothDisabled: boolean
  factoryResetDisabled: boolean
  modifyAccountsDisabled: boolean
  autoDateAndTimeZone: 'AUTO_DATE_AND_TIME_ZONE_USER_CHOICE'|'AUTO_DATE_AND_TIME_ZONE_ENFORCED'
  deviceConnectivityManagement: DeviceConnectionPolicy
  advancedSecurityOverrides: {
    developerSettings: 'DEVELOPER_SETTINGS_DISABLED'|'DEVELOPER_SETTINGS_ALLOWED'
  }
}

export type {
  Resp, Alert, Manager, Enterprise, Device,
  ApplicationPolicy, PasswordPolicy, DeviceConnectionPolicy, Policy
}
