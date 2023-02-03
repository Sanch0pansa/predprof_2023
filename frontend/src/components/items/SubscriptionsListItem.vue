<template>
  <Block :class="['sm d-flex justify-content-between align-items-center']">
    <RouterLink :to="href">{{ name }}</RouterLink>
    <div class="d-flex align-items-center gap-3">
      <Indicator :status="status"></Indicator>
      <i class="fas fa-ban text-danger"></i>
    </div>


  </Block>
</template>

<script>

export default {
  name: "SubscriptionsListItem",
  props: {
    status: [Number],
    href: [String],
    name: [String],
  }
}
</script>

<style scoped>

</style>