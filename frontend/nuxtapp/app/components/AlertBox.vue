<script setup lang="ts">
  defineProps<{alert: Alert}>()
</script>


<template>
  <div v-if="alert.show" class="alert alert-danger mb-3" role="alert">
    ※ {{ alert.msg }}
  </div>
</template>
