<script setup lang="ts">
  useHead({title: '組織の作成'})

  let alert: Ref<Alert> = ref({
    show: false,
    msg: ''
  })

  const resp: Resp = await accessManagerGoogleSignupGet()

  const signup_url: string = resp.status === 200 ? resp.json.google_signup.url : 'URLの取得失敗 ページを更新してください'
  const signup_url_name: string = resp.status === 200 ? resp.json.google_signup.name : ''

  const enterprise_token: Ref<string> = ref('')

  async function tryCreateEnterprise(): Promise<void> {
    const resp: Resp = await accessEnterprisePost(
      signup_url_name, enterprise_token.value
    )
    if (resp.status === 200) {
      useRouter().push({name: 'index'})
    }
    else {
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
    組織の作成
  </h4>
  <div class="mb-4">
    Googleサインアップ (ページを更新するとリンクが変わるので注意)<br>
    <a :href="signup_url" target="_blank" class="fw-bolder text-break">{{ signup_url }}</a>
  </div>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div class="mb-4">
      <label class="mb-2">組織トークン</label>
      <input type="text" class="form-control border border-primary"
        placeholder="Googleから提示されたコードを貼り付け"
        v-model="enterprise_token"
      />
    </div>
    <div>
      <button class="btn btn-primary"
        :disabled="!/^[a-zA-Z0-9.\-_/]+$/.test(signup_url_name) || !/^[a-zA-Z0-9\-_]+$/.test(enterprise_token)"
        @click="tryCreateEnterprise"
      >
        新規作成
      </button>
    </div>
  </div>
</template>
