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

export type {
  Resp, Alert, Manager, Enterprise, Device
}
