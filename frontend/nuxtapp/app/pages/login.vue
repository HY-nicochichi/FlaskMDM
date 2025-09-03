<script setup lang="ts">
  import AlertBox from '~/components/AlertBox.vue'
  import {LoadingSpinner} from '~/components/SvgIcons'
  import {accessManagerAccessTokenPost} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import type {Alert, Resp} from '~/types'

  useHead({title: 'ログイン'})

  let alert: Ref<Alert> = ref({
    show: false, msg: ''
  })

  let id: Ref<string> = ref('')
  let password: Ref<string> = ref('')

  const invalid: ComputedRef<boolean> = computed(() =>
    !/^[a-z0-9.@]+$/.test(id.value) || !/^[a-zA-Z0-9]+$/.test(password.value)
  )
  const submitting: Ref<boolean> = ref(false)

  async function tryLogin(): Promise<void> {
    submitting.value = true
    const resp: Resp = await accessManagerAccessTokenPost(
      id.value, password.value
    )
    if (resp.status === 200) {
      setJwt(resp.json.access_token)
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
    ログイン
  </h4>
  <div class="col-sm-9 col-md-7 col-lg-5 border border-primary bg-light p-3">
    <div class="mb-4">
      <label class="mb-2">ID / メールアドレス</label>
      <input type="text" class="form-control border border-primary" v-model="id" placeholder="a-zと0-9と.と@"/>
    </div>
    <div class="mb-4">
      <label class="mb-2">パスワード</label>
      <input type="password" class="form-control border border-primary" v-model="password" placeholder="a-zとA-Zと0-9"/>
    </div>
    <br>
    <div>
      <button class="btn btn-primary"
        @click="tryLogin" :disabled="invalid || submitting"
      >
        <LoadingSpinner
          v-if="submitting" class="mx-3" :size="'25'" :color="'white'"
        />
        <span v-else>ログイン</span>
      </button>
    </div>
  </div>
</template>
