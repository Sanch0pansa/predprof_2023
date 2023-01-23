<template>
  <a :href="href" class="text-primary">
    <slot></slot>
  </a>
</template>

<script>
export default {
  name: "Link",
  props: {
    href: {
      required: true,
    }
  }
}
</script>

<style scoped>

</style>