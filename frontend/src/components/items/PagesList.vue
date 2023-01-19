<template>
<div class="d-flex flex-column gap-3">
  <PagesListItem v-for="obj in [0, 1, 2]" :status="obj" :href="`https://google.com`"></PagesListItem>
</div>
</template>

<script>
import PagesListItem from "@/components/items/PagesListItem.vue";

export default {
  components: {PagesListItem},
  name: "PagesList"
}
</script>

<style scoped>

</style>