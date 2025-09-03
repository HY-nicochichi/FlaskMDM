<script setup lang="ts">
  useHead({title: 'ログイン'})

  let alert: Ref<Alert> = ref({
    show: false,
    msg: ''
  })

  let id: Ref<string> = ref('')
  let password: Ref<string> = ref('')

  async function tryLogin(): Promise<void> {
    const resp: Resp = await accessManagerAccessTokenPost(
      id.value, password.value
    )
    if (resp.status === 200) {
      setJwt(resp.json.access_token)
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
        @click="tryLogin"
        :disabled="!/^[a-z0-9.@]+$/.test(id) || !/^[a-zA-Z0-9]+$/.test(password)"
      >
        ログイン
      </button>
    </div>
  </div>
</template>
