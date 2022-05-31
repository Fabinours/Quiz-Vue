<template>
  <div>
    <AppHeader/>
    <div class="mx-2 my-5">
      <router-view/>
    </div>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';

export default {
    name: "App",
    components: { AppHeader }
}
</script>