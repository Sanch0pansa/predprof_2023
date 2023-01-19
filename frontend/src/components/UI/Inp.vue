<template>
  <div class="">
    <label :for="name">{{ label }}</label>
    <input :type="type" class="form-control" :name="name" :id="name">
  </div>
</template>

<script>
export default {
  name: "Inp",
  props: {
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      required: false,
      default: "string"
    }
  }
}
</script>

<style scoped>

</style>