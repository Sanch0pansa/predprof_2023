<template>
  <Block :class="['sm d-flex justify-content-between align-items-center']">
    <RouterLink :to="href">{{ name }}</RouterLink>
    <div class="d-flex align-items-center gap-3">
      <Indicator :status="status"></Indicator>
      <i @click="unsubscribe" class="fas fa-ban text-danger" role="button"></i>
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
  },
  methods: {

    async unsubscribe(ev) {
      this.$emit('unsubscribe', ev);
    },
  }
}
</script>

<style scoped>

</style>