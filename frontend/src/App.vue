<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <a-config-provider
    :theme="{
      token: {
        colorPrimary: '#1890ff',
      },
    }"
  >
    <RouterView />
  </a-config-provider>
</template>

<style>
#app {
  min-height: 100vh;
  background-color: #f5f5f5;
}
</style>
