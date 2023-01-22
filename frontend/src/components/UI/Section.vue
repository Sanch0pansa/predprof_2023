<template>
<div class="mt-5">
  <h4 class="mb-3">{{ title }}</h4>
  <slot></slot>
</div>
</template>

<script>
export default {
  name: "PageSection",
  props: {
    title: {
      required: true
    }
  }
}
</script>

<style scoped>

</style>