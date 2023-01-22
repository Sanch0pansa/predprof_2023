<template>
  <button v-if="href == ''" class="btn btn-primary">
    <slot></slot>
  </button>
  <a v-else :href="href" class="btn btn-primary">
    <slot></slot>
  </a>
</template>

<script>
export default {
  name: "Btn",
  props: {
    href: {
      required: false,
      default: ""
    }
  }
}
</script>

<style scoped>

</style>