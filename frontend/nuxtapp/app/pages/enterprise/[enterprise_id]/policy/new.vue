<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {accessPolicyPatch} from '~/composables/ApiClient'
  import type {Alert, Resp, Policy, ApplicationPolicy, PasswordPolicy} from '~/types'

  const enterprise_id: string = useRoute().params.enterprise_id as string ?? ''
  
  useHead({title: 'ポリシーの作成'})

  const alert: Ref<Alert> = ref({
    show: false,
    msg: ''
  })

  const policy_id: Ref<string> = ref('')

  const policyData: Ref<Policy> = ref({
    applications: [
      {
        packageName: 'com.android.chrome',
        installType: 'FORCE_INSTALLED'
      }
    ],
    passwordPolicies: [
      {
        passwordMinimumLength: 16,
        passwordQuality: 'ALPHANUMERIC',
        maximumFailedPasswordsForWipe: 2
      }
    ],
    cameraAccess: 'CAMERA_ACCESS_DISABLED',
    microphoneAccess: 'MICROPHONE_ACCESS_DISABLED',
    systemUpdate: {
      type: 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'
    },
    screenCaptureDisabled: true,
    smsDisabled: true,
    bluetoothDisabled: true,
    factoryResetDisabled: true,
    modifyAccountsDisabled: true,
    autoDateAndTimeZone: 'AUTO_DATE_AND_TIME_ZONE_USER_CHOICE',
    deviceConnectivityManagement: {
      usbDataAccess: 'DISALLOW_USB_FILE_TRANSFER',
      tetheringSettings: 'DISALLOW_ALL_TETHERING',
      wifiSsidPolicy: {
        wifiSsidPolicyType: 'WIFI_SSID_DENYLIST',
        wifiSsids: [] as {wifiSsid: string}[]
      }
    },
    advancedSecurityOverrides: {
      developerSettings: 'DEVELOPER_SETTINGS_DISABLED'
    }
  })

  const invalid: ComputedRef<boolean> = computed(() =>
    !/^[a-z0-9_]+$/.test(policy_id.value) || 
    !(
      (policyData.value.applications[0] as ApplicationPolicy).managedConfiguration === undefined ||
      (policyData.value.applications[0] as ApplicationPolicy).managedConfiguration?.URLAllowlist.every(
        domain => /^[a-zA-Z0-9.:/-]+$/.test(domain)
      )
    ) ||
    !policyData.value.applications.every(
      application => /^[a-z0-9.-]+$/.test(application.packageName)
    ) || 
    !policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids.every(
      ({wifiSsid: value}) => (/^[ -~]+$/.test(value) && value.length < 33)
    )
  )
  const submitting: Ref<boolean> = ref(false)

  const tempURLAllowlist: Ref<string[]|null> = ref(null)
  const tempWifiSsids: Ref<{wifiSsid: string}[]|null> = ref(null)

  const isSiteRestrictionEnabled = computed({
    get: () => (policyData.value.applications[0] as ApplicationPolicy).managedConfiguration !== undefined,
    set: (value: boolean) => {
      if (value) {
        (policyData.value.applications[0] as ApplicationPolicy).managedConfiguration = {
          URLBlocklist: ['*'],
          URLAllowlist: tempURLAllowlist.value ?? ['']
        }
        tempURLAllowlist.value = null
      }
      else {
        tempURLAllowlist.value = (
          policyData.value.applications[0] as ApplicationPolicy
        ).managedConfiguration?.URLAllowlist ?? []
        delete (policyData.value.applications[0] as ApplicationPolicy).managedConfiguration
      }
    }
  })

  const isSsidRestrictionEnabled = computed({
    get: () => policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsidPolicyType === 'WIFI_SSID_ALLOWLIST',
    set: (value: boolean) => {
      policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsidPolicyType = value ? 'WIFI_SSID_ALLOWLIST' : 'WIFI_SSID_DENYLIST'
      if (value) {
        policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids = tempWifiSsids.value ?? [{wifiSsid: ''}]
        tempWifiSsids.value = null
      } else {
        tempWifiSsids.value = policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids
        policyData.value.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids = []
      }
    }
  })

  const isCameraEnabled = computed({
    get: () => policyData.value.cameraAccess === 'CAMERA_ACCESS_USER_CHOICE',
    set: (value: boolean) => {
      policyData.value.cameraAccess = value ? 'CAMERA_ACCESS_USER_CHOICE' : 'CAMERA_ACCESS_DISABLED'
    }
  })

  const isScreenShotEnabled = computed({
    get: () => !policyData.value.screenCaptureDisabled,
    set: (value: boolean) => {
      policyData.value.screenCaptureDisabled = !value
    }
  })

  const isMicrophoneEnabled = computed({
    get: () => policyData.value.microphoneAccess === 'MICROPHONE_ACCESS_USER_CHOICE',
    set: (value: boolean) => {
      policyData.value.microphoneAccess = value ? 'MICROPHONE_ACCESS_USER_CHOICE' : 'MICROPHONE_ACCESS_DISABLED'
    }
  })

  const isBluetoothEnabled = computed({
    get: () => !policyData.value.bluetoothDisabled,
    set: (value: boolean) => {
      policyData.value.bluetoothDisabled = !value
    }
  })

  const isTetheringEnabled = computed({
    get: () => policyData.value.deviceConnectivityManagement.tetheringSettings === 'ALLOW_ALL_TETHERING',
    set: (value: boolean) => {
      policyData.value.deviceConnectivityManagement.tetheringSettings = value ? 'ALLOW_ALL_TETHERING' : 'DISALLOW_ALL_TETHERING'
    }
  })

  const isSmsEnabled = computed({
    get: () => !policyData.value.smsDisabled,
    set: (value: boolean) => {
      policyData.value.smsDisabled = !value
    }
  })

  const isFactoryResetEnabled = computed({
    get: () => !policyData.value.factoryResetDisabled,
    set: (value: boolean) => {
      policyData.value.factoryResetDisabled = !value
    }
  })

  const isModifyAccountsEnabled = computed({
    get: () => !policyData.value.modifyAccountsDisabled,
    set: (value: boolean) => {
      policyData.value.modifyAccountsDisabled = !value
    }
  })

  const isSystemAutoUpdateEnabled = computed({
    get: () => policyData.value.systemUpdate.type === 'AUTOMATIC',
    set: (value: boolean) => {
      policyData.value.systemUpdate.type = value ? 'AUTOMATIC' : 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'
    }
  })

  const isAutoDateEnabled = computed({
    get: () => policyData.value.autoDateAndTimeZone === 'AUTO_DATE_AND_TIME_ZONE_ENFORCED',
    set: (value: boolean) => {
      policyData.value.autoDateAndTimeZone = value ? 'AUTO_DATE_AND_TIME_ZONE_ENFORCED' : 'AUTO_DATE_AND_TIME_ZONE_USER_CHOICE'
    }
  })

  const isDeveloperModeEnabled = computed({
    get: () => policyData.value.advancedSecurityOverrides.developerSettings === 'DEVELOPER_SETTINGS_ALLOWED',
    set: (value: boolean) => {
      policyData.value.advancedSecurityOverrides.developerSettings = value ? 'DEVELOPER_SETTINGS_ALLOWED' : 'DEVELOPER_SETTINGS_DISABLED'
    }
  })

  const isUsbFileAccessEnabled = computed({
    get: () => policyData.value.deviceConnectivityManagement.usbDataAccess === 'ALLOW_USB_DATA_TRANSFER',
    set: (value: boolean) => {
      policyData.value.deviceConnectivityManagement.usbDataAccess = value ? 'ALLOW_USB_DATA_TRANSFER' : 'DISALLOW_USB_FILE_TRANSFER'
    }
  })

  async function tryCreatePolicy() {
    submitting.value = true
    const resp: Resp = await accessPolicyPatch(
      enterprise_id, policy_id.value, policyData.value
    )
    if (resp.status === 200) {
      useRouter().push('/enterprise/' + enterprise_id)
    } else {
      submitting.value = false
      alert.value = {
        show: true,
        msg: resp.json.msg
      }
    }
  }
</script>


<template>
  <AlertBox :alert="alert"/>
  <h4 class="fw-bolder mb-3">
    ポリシーの作成
  </h4>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div class="mb-4">
      <label for="policyName" class="form-label fw-bolder">ポリシーID</label>
      <input type="text" class="form-control"
        v-model="policy_id" placeholder="a-zと0-9と_"
      >
    </div>
    <div class="mb-4">
      <label for="policyName" class="form-label fw-bolder">
        アプリケーション<br>
        <span>
          <a href="https://play.google.com/work/apps" target="_blank" class="text-break">
            https://play.google.com/work/apps
          </a> 
          でアプリを検索
        </span>
      </label>
      <div v-for="(application, index) in policyData.applications" class="mb-2">
        <div v-if="index === 0">
          <div class="d-flex align-items-center">
            <input type="text" class="form-control flex-grow-1" :value="application.packageName" disabled>
            <button class="btn btn-danger btn-sm ms-2 flex-shrink-0" disabled>
              削除
            </button>
          </div>
          <div class="form-check form-switch my-2 ms-3">
            <input class="form-check-input" type="checkbox" role="switch" id="siteRestrictionToggle" v-model="isSiteRestrictionEnabled">
            <label class="form-check-label" for="siteRestrictionToggle">WEBサイト制限</label>
          </div>
          <div v-if="application.managedConfiguration !== undefined" class="ms-3">
            <label for="wifiSsids" class="form-label fw-bolder">閲覧許可サイト</label>
            <div v-for="(domain, index) in application.managedConfiguration.URLAllowlist" class="d-flex align-items-center mb-2">
              <input type="text" class="form-control flex-grow-1"
                v-model="application.managedConfiguration.URLAllowlist[index]" placeholder="https://allowed.site.domain"
              >
              <button
                class="btn btn-danger btn-sm ms-2 flex-shrink-0"
                @click="application.managedConfiguration.URLAllowlist.splice(index, 1)"
              >
                削除
              </button>
            </div>
            <div>
              <button type="button" class="btn btn-primary btn-sm my-2"
                @click="application.managedConfiguration.URLAllowlist.push('')"
              >
                ＋ 追加
              </button>
            </div>
          </div>
        </div>
        <div v-else class="d-flex align-items-center">
          <input type="text" class="form-control flex-grow-1"
            v-model="application.packageName" placeholder="アプリのURLの?id=以降を貼り付け"
          >
          <button
            class="btn btn-danger btn-sm ms-2 flex-shrink-0"
            @click="policyData.applications.splice(index, 1)"
          >
            削除
          </button>
        </div>
      </div>
      <div>
        <button type="button" class="btn btn-primary btn-sm mt-2"
          @click="policyData.applications.push(
            {packageName: '', installType: 'FORCE_INSTALLED'}
          )"
        >
          ＋ 追加
        </button>
      </div>
    </div>
    <div class="mb-4">
      <h5 class="fw-bolder">パスワード</h5>
      <div class="mb-3">
        <label for="minLength" class="form-label">最小文字数 (4-16)</label>
        <input
          type="number"
          class="form-control"
          id="minLength"
          v-model.number="(policyData.passwordPolicies[0] as PasswordPolicy).passwordMinimumLength"
          min="4"
          max="16"
        >
      </div>
      <div class="mb-3">
        <label for="failedAttempts" class="form-label">失敗回数上限 (2-10)</label>
        <input
          type="number"
          class="form-control"
          id="failedAttempts"
          v-model.number="(policyData.passwordPolicies[0] as PasswordPolicy).maximumFailedPasswordsForWipe"
          min="2"
          max="10"
        >
      </div>
      <div class="mb-3">
        <label for="passwordQuality" class="form-label">パスワード形式</label>
        <select class="form-select" id="passwordQuality" v-model="(policyData.passwordPolicies[0] as PasswordPolicy).passwordQuality">
          <option value="NUMERIC">数字のみ</option>
          <option value="ALPHABETIC">英字のみ</option>
          <option value="ALPHANUMERIC">英数字</option>
        </select>
      </div>
    </div>
    <div class="mb-4">
      <h5 class="fw-bolder">Wi-Fi接続設定</h5>
      <div class="form-check form-switch">
        <input class="form-check-input" type="checkbox" role="switch" id="ssidRestrictionToggle" v-model="isSsidRestrictionEnabled">
        <label class="form-check-label" for="ssidRestrictionToggle">SSID制限</label>
      </div>
      <div v-if="policyData.deviceConnectivityManagement.wifiSsidPolicy.wifiSsidPolicyType === 'WIFI_SSID_ALLOWLIST'" class="mt-3">
        <label for="wifiSsids" class="form-label fw-bolder">接続許可SSID</label>
        <div v-for="(ssid, index) in policyData.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids" class="d-flex align-items-center mb-2">
          <input type="text" class="form-control flex-grow-1" v-model="ssid.wifiSsid" placeholder="許可したいSSID">
          <button
            class="btn btn-danger btn-sm ms-2 flex-shrink-0" :disabled="index === 0"
            @click="policyData.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids.splice(index, 1)"
          >
            削除
          </button>
        </div>
        <div>
          <button type="button" class="btn btn-primary btn-sm mt-2"
            @click="policyData.deviceConnectivityManagement.wifiSsidPolicy.wifiSsids.push({wifiSsid: ''})"
          >
            ＋ 追加
          </button>
        </div>
      </div>
    </div>
    <div class="mb-4">
      <h5 class="fw-bolder">各種機能の有効/無効</h5>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="cameraToggle" v-model="isCameraEnabled">
        <label class="form-check-label" for="cameraToggle">カメラ</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="screenCaptureToggle" v-model="isScreenShotEnabled">
        <label class="form-check-label" for="screenCaptureToggle">スクリーンショット</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="microphoneToggle" v-model="isMicrophoneEnabled">
        <label class="form-check-label" for="microphoneToggle">マイク</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="bluetoothToggle" v-model="isBluetoothEnabled">
        <label class="form-check-label" for="bluetoothToggle">Bluetooth</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="tetheringToggle" v-model="isTetheringEnabled">
        <label class="form-check-label" for="tetheringToggle">テザリング</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="smsToggle" v-model="isSmsEnabled">
        <label class="form-check-label" for="smsToggle">SMS</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="factoryResetToggle" v-model="isFactoryResetEnabled">
        <label class="form-check-label" for="factoryResetToggle">デバイス初期化</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="modifyAccountsToggle" v-model="isModifyAccountsEnabled">
        <label class="form-check-label" for="modifyAccountsToggle">アカウント追加/削除</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="systemUpdateToggle" v-model="isSystemAutoUpdateEnabled">
        <label class="form-check-label" for="systemUpdateToggle">OS自動更新</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="autoDateToggle" v-model="isAutoDateEnabled">
        <label class="form-check-label" for="autoDateToggle">時刻自動設定</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="developerModeToggle" v-model="isDeveloperModeEnabled">
        <label class="form-check-label" for="developerModeToggle">開発者オプション</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="usbFileToggle" v-model="isUsbFileAccessEnabled">
        <label class="form-check-label" for="usbFileToggle">USBファイル送受信</label>
      </div>
    </div>
    <br>
    <button type="submit" class="btn btn-primary me-3"
      @click="tryCreatePolicy" :disabled="invalid || submitting"
    >
      <LoadingSpinner
        v-if="submitting" class="mx-3" :size="'25'" :color="'white'"
      />
      <span v-else>新規作成</span>
    </button>
  </div>
</template>
