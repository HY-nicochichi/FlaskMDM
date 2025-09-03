<script setup lang="ts">
  import {BrandLogo, HamburgerMenu} from '~/components/SvgIcons'
  import {accessManagerDelete} from '~/composables/ApiClient'
  import {setJwt} from '~/composables/JwtManager'
  import {useManagerStore} from '~/stores'
  
  function tryLogout(): void {
    setJwt()
    useRouter().push({name: 'login'})
  }

  async function confirmDeleteManager(): Promise<void> {
    if (confirm('本当にアカウントを削除しますか？')) {
      await accessManagerDelete()
      setJwt()
      useRouter().push({name: 'login'})
    }
  }
</script>


<template>
  <div class="pt-3">
    <nav class="navbar navbar-expand-sm navbar-dark bg-dark px-3 py-2">
      <NuxtLink to="/" class="navbar-brand color-dark d-flex align-items-center">
        <BrandLogo :size="'35'" :color="'mediumspringgreen'"/>
        <span class="ps-2 fs-4 fw-bolder">Flask MDM</span>
      </NuxtLink>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#NavBarContent" aria-controls="NavBarContent" aria-expanded="false" aria-label="Toggle navigation">
        <HamburgerMenu :size="'35'" :color="'white'"/>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="NavBarContent">
        <ul v-if="useManagerStore().value.login" class="navbar-nav">
          <li class="nav-item">
            <NuxtLink class="nav-link active fw-bolder me-2" @click="tryLogout">
              ログアウト
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink class="nav-link active fw-bolder me-2" @click.prevent="confirmDeleteManager">
              管理者アカウント削除
            </NuxtLink>
          </li>
        </ul>
        <ul v-else class="navbar-nav">
          <li class="nav-item">
            <NuxtLink to="/login" class="nav-link active fw-bolder me-2">
              ログイン
            </NuxtLink>
          </li>
          <li class="nav-item">
            <NuxtLink to="/new_manager" class="nav-link active fw-bolder">
              管理者アカウント登録
            </NuxtLink>
          </li>
        </ul>
      </div>
    </nav>
  </div>
</template>
