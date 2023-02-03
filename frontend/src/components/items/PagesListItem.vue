<template>
<Block :class="['sm d-flex justify-content-between align-items-center']">
  <RouterLink :to="href">{{ name }}</RouterLink>
  <Indicator :status="status"></Indicator>
</Block>
</template>

<script>

export default {
  name: "PagesListItem",
  props: {
    status: [Number],
    href: [String],
    name: [String],
  }
}
</script>

<style scoped>

</style>