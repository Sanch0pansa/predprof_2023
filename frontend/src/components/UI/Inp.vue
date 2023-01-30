<template>
  <div class="">
    <label :for="name">{{ label }}</label>
    <input :value="modelValue" @input="updateInput" :type="type" :class="{
      'form-control': true,
      'is-invalid': errors.length
     }" :name="name" :id="name">
      <div  v-for="error in errors" class="text-start invalid-feedback">
        {{ error }}
      </div>
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
    errors: {
      type: Array,
      required: false,
      default: [],
    },
    modelValue: [],

  },
  methods: {
    updateInput(event) {
      this.$emit("update:modelValue", event.target.value);
      this.$emit("update:errors", []);
    }
  }
}
</script>

<style scoped>

</style>