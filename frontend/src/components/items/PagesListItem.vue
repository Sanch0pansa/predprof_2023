<template>
<Block :class="['sm d-flex justify-content-between align-items-center']">
  <Link :href="href">{{ name }}</Link>
  <div class="indicator"
       :class="{
    'indicator-success': status == 2,
    'indicator-warning': status == 1,
    'indicator-danger': status == 0,
    'indicator-secondary': status == 3
  }">

  </div>
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