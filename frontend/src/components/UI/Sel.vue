<template>
  <div class="">
    <label :for="name">{{ label }}</label>
    <select :value="modelValue" @change="updateSelect" :type="type" class="form-control" :name="name" :id="name">
      <option v-for="option in options" :value="option.value">{{ option.text }}</option>
    </select>
  </div>
</template>

<script>
export default {
  name: "Sel",
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
    options: [],
  },

  methods: {
    updateSelect(event) {
      this.$emit("update:modelValue", event.target.value);
    }
  }
}
</script>

<style scoped>

</style>