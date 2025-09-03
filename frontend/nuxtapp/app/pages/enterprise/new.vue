<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {accessManagerGoogleSignupGet, accessEnterprisePost} from '~/composables/ApiClient'
  import type {Alert, Resp} from '~/types'

  useHead({title: '組織の作成'})

  let alert: Ref<Alert> = ref({
    show: false, msg: ''
  })

  const resp: Resp = await accessManagerGoogleSignupGet()

  const signup_url: string = resp.status === 200 ? resp.json.google_signup.url : 'URLの取得失敗 ページを更新してください'
  const signup_url_name: string = resp.status === 200 ? resp.json.google_signup.name : ''

  const enterprise_token: Ref<string> = ref('')

  const invalid: ComputedRef<boolean> = computed(() =>
    !/^[a-zA-Z0-9.\-_/]+$/.test(signup_url_name) || !/^[a-zA-Z0-9\-_]+$/.test(enterprise_token.value)
  )
  const submitting: Ref<boolean> = ref(false)

  async function tryCreateEnterprise(): Promise<void> {
    submitting.value = true
    const resp: Resp = await accessEnterprisePost(
      signup_url_name, enterprise_token.value
    )
    if (resp.status === 200) {
      useRouter().push({name: 'index'})
    }
    else {
      submitting.value = false
      alert.value = {
        show: true, msg: resp.json.msg
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
        @click="tryCreateEnterprise" :disabled="invalid || submitting"
      >
        <LoadingSpinner
          v-if="submitting" class="mx-3" :size="'25'" :color="'white'"
        />
        <span v-else>新規作成</span>
      </button>
    </div>
  </div>
</template>
