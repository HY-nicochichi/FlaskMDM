<script setup lang="ts">
  const enterprise_id: string = useRoute().params.enterprise_id as string ?? ''
  const policy_id: string = useRoute().params.policy_id as string ?? ''

  useHead({title: 'ポリシー: ' + policy_id})

  const alert: Ref<Alert> = ref({
    show: false, msg: ''
  })

  const policyData = ref({
    applications: [
      {
        packageName: '',
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
    systemUpdate: {
      type: 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'
    },
    screenCaptureDisabled: true,
    smsDisabled: true,
    bluetoothDisabled: true,
    factoryResetDisabled: true
  })

  const resp: Resp = await accessPolicyGet(enterprise_id, policy_id)

  if (resp.status === 200) {
    policyData.value = resp.json.policy
  } else {
    alert.value = {
      show: true, msg: resp.json.msg
    }
  }

  const isCameraEnabled = computed({
    get: () => policyData.value.cameraAccess === 'CAMERA_ACCESS_USER_CHOICE',
    set: (value: boolean) => {
      policyData.value.cameraAccess = value ? 'CAMERA_ACCESS_USER_CHOICE' : 'CAMERA_ACCESS_DISABLED'
    }
  })

  const isBluetoothEnabled = computed({
    get: () => !policyData.value.bluetoothDisabled,
    set: (value: boolean) => {
      policyData.value.bluetoothDisabled = !value
    }
  })

  const isScreenShotEnabled = computed({
    get: () => !policyData.value.screenCaptureDisabled,
    set: (value: boolean) => {
      policyData.value.screenCaptureDisabled = !value
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

  const isSystemAutoUpdateEnabled = computed({
    get: () => policyData.value.systemUpdate.type === 'AUTOMATIC',
    set: (value: boolean) => {
      policyData.value.systemUpdate.type = value ? 'AUTOMATIC' : 'SYSTEM_UPDATE_TYPE_UNSPECIFIED'
    }
  })

  async function tryUpdatePolicy() {
    const resp: Resp = await accessPolicyPatch(
      enterprise_id, policy_id, policyData.value
    )
    if (resp.status === 200) {
      useRouter().push('/enterprise/' + enterprise_id)
    }
    else {
      alert.value = {
        show: true, msg: resp.json.msg
      }
    }
  }

  async function tryDeletePolicy() {
    if (confirm('本当にポリシーを削除しますか？')) {
      await accessPolicyDelete(enterprise_id, policy_id)
      useRouter().push('/enterprise/' + enterprise_id)
    }
  }
</script>

<template>
  <AlertBox :alert="alert"/>
  <h4 class="fw-bolder mb-3">
    ポリシーの編集
  </h4>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div class="mb-4">
      <label for="policyName" class="form-label fw-bolder">ポリシーID</label>
      <input type="text" class="form-control" :value="policy_id" disabled>
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
      <div v-for="(application, index) in policyData.applications" class="d-flex align-items-center mb-2">
        <input type="text" class="form-control flex-grow-1" v-model="application.packageName" placeholder="アプリのURLの?id=以降を貼り付け">
        <button
          class="btn btn-danger btn-sm ms-2 flex-shrink-0"
          @click="policyData.applications.splice(index, 1)"
        >
          削除
        </button>
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
      <h5 class="fw-bolder">各種機能の有効/無効</h5>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="cameraToggle" v-model="isCameraEnabled">
        <label class="form-check-label" for="cameraToggle">カメラ</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="bluetoothToggle" v-model="isBluetoothEnabled">
        <label class="form-check-label" for="bluetoothToggle">Bluetooth</label>
      </div>
      <div class="form-check form-switch my-2">
        <input class="form-check-input" type="checkbox" role="switch" id="screenCaptureToggle" v-model="isScreenShotEnabled">
        <label class="form-check-label" for="screenCaptureToggle">スクリーンショット</label>
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
        <input class="form-check-input" type="checkbox" role="switch" id="systemUpdateToggle" v-model="isSystemAutoUpdateEnabled">
        <label class="form-check-label" for="systemUpdateToggle">OS自動更新</label>
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
    <br>
    <button type="submit" class="btn btn-primary me-3"
      :disabled="!policyData.applications.every(
        application => /^[a-z0-9.-]+$/.test(application.packageName)
      )"
      @click="tryUpdatePolicy"
    >
      更新
    </button>
    <button type="button" class="btn btn-danger" @click.prevent="tryDeletePolicy">
      ポリシーを削除
    </button>
  </div>
</template>
