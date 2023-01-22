<template>
  <form @submit.prevent="submit" action="" enctype="multipart/form-data">
    <slot></slot>
  </form>
</template>

<script>
export default {
  name: "FormEl",
  methods: {
    submit(ev) {
      this.$emit('handle');
    }
  }
}
</script>

<style scoped>

</style>