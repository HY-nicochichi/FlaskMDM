<script setup lang="ts">
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
      <a class="navbar-brand color-dark d-flex align-items-center" href="/">
        <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 24 24" style="color:mediumspringgreen">
          <path fill="currentColor" d="M1 18q.225-2.675 1.638-4.925T6.4 9.5L4.55 6.3q-.15-.225-.075-.475T4.8 5.45q.2-.125.45-.05t.4.3L7.5 8.9Q9.65 8 12 8t4.5.9l1.85-3.2q.15-.225.4-.3t.45.05q.25.125.325.375t-.075.475L17.6 9.5q2.35 1.325 3.762 3.575T23 18zm6-2.75q.525 0 .888-.363T8.25 14t-.363-.888T7 12.75t-.888.363T5.75 14t.363.888t.887.362m10 0q.525 0 .888-.363T18.25 14t-.363-.888T17 12.75t-.888.363t-.362.887t.363.888t.887.362"/>
        </svg>
        <span class="ps-2 fs-4 fw-bolder">Flask MDM</span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#NavBarContent" aria-controls="NavBarContent" aria-expanded="false" aria-label="Toggle navigation">
        <svg xmlns="http://www.w3.org/2000/svg" width="35" height="35" viewBox="0 0 16 16" style="color:white">
          <path fill="currentColor" fill-rule="evenodd" d="M2.5 12a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5m0-4a.5.5 0 0 1 .5-.5h10a.5.5 0 0 1 0 1H3a.5.5 0 0 1-.5-.5"/>
        </svg>
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
