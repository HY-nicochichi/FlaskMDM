<script setup lang="ts">
  import NavBar from '~/components/NavBar.vue'
</script>


<template>
  <div>
    <NuxtLoadingIndicator
      color="deepskyblue" :height="5"
    />
    <NavBar/>
    <div class="px-3 py-4">
      <NuxtPage/>
    </div>
  </div>
</template>
