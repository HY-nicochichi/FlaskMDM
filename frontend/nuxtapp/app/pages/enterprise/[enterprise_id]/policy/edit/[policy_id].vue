<script setup lang="ts">
  const enterprise_id: string = useRoute().params.enterprise_id as string ?? ''
  const policy_id: string = useRoute().params.policy_id as string ?? ''

  useHead({title: 'ポリシー: ' + policy_id})

  const alert: Ref<Alert> = ref({
    show: false,
    msg: ''
  })

  const policyData: Ref<{
    id: string,
    applications: {packageName: string}[]
  }> = ref({
    id: policy_id,
    applications: [{packageName: ''}]
  })

  policyData.value.applications = [
    {packageName: 'com.android.chrome'}, {packageName: 'com.android.instagram'}
  ]
  const resp: Resp = await accessPolicyGet(enterprise_id, policy_id)

  if (resp.status === 200) {
    const policyFromApi: any = resp.json.policy
    policyData.value.applications = policyFromApi.applications.map(
        (application: any) => ({packageName: application.packageName})
    )
  } else {
    alert.value = {
        show: true,
        msg: resp.json.msg
    }
  }

  const policyPayload = computed(() => {
    return {
      applications: policyData.value.applications.map(
        application => ({
          packageName: application.packageName,
          installType: "FORCE_INSTALLED"
        })
      )
    }
  })

  function addApplication() {
    policyData.value.applications.push({packageName: ''})
  }

  function removeApplication(index: number) {
    if (policyData.value.applications.length > 0) {
      policyData.value.applications.splice(index, 1)
    }
  }

  async function tryUpdatePolicy() {
    const resp: Resp = await accessPolicyPatch(
      enterprise_id, policyData.value.id, policyPayload.value
    )
    if (resp.status === 200) {
      useRouter().push('/enterprise/' + enterprise_id)
    }
    else {
      alert.value = {
        show: true,
        msg: resp.json.msg
      }
    }
  }

  async function tryDeletePolicy() {
    if (confirm('本当にポリシーを削除しますか？')) {
      await accessPolicyDelete(enterprise_id, policyData.value.id)
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
      <input type="text" class="form-control" v-model="policyData.id" disabled>
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
        <input type="text" class="form-control flex-grow-1" v-model="application.packageName" placeholder="アプリのURLの?id=以後を貼り付け">
        <button
          class="btn btn-danger btn-sm ms-2 flex-shrink-0"
          @click="removeApplication(index)"
        >
          削除
        </button>
      </div>
      <div>
        <button type="button" class="btn btn-primary btn-sm mt-2" @click="addApplication">
          ＋ 追加
        </button>
      </div>
    </div>
    <br>
    <button type="submit" class="btn btn-primary me-3"
      :disabled="!policyData.applications.every(application => /^[a-z0-9.-]+$/.test(application.packageName))"
      @click="tryUpdatePolicy"
    >
      更新
    </button>
    <button type="button" class="btn btn-danger" @click.prevent="tryDeletePolicy">
      ポリシーを削除
    </button>
  </div>
</template>
