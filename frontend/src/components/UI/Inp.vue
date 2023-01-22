<template>
  <div class="">
    <label :for="name">{{ label }}</label>
    <input :value="modelValue" @input="updateInput" :type="type" class="form-control" :name="name" :id="name">
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
    },
    modelValue: [],

  },
  methods: {
    updateInput(event) {
      this.$emit("update:modelValue", event.target.value);
    }
  }
}
</script>

<style scoped>

</style>