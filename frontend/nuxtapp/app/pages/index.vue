<script setup lang="ts">
  import {useManagerStore} from '~/stores'

  useHead({title: 'Flask MDM'})
</script>


<template>
  <div class="fs-5 fw-bolder">
    管理者ID： {{ useManagerStore().value.id }}
  </div>
  <div class="fs-5 mt-4 fw-bolder">
    組織 (Android Enterprise)
  </div>
  <div class="ms-3 mt-2" v-for="enterprise in useManagerStore().value.enterprises">
    <div class="mt-2">
      <NuxtLink :to="'/enterprise/' + enterprise.id" class="text-decoration-none fw-bolder">
        {{ enterprise.name }} ({{ enterprise.id }})
      </NuxtLink>
    </div>
  </div>
  <div class="mt-3">
    <NuxtLink to="/enterprise/new" class="btn btn-primary" href="/enterprise/new">＋ 作成</NuxtLink>
  </div>
</template>
