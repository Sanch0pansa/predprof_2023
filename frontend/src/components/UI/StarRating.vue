<template>
  <div class="">
    <label>{{ label }}</label><br>
    <div class="d-inline-flex bg-light rounded gap-2 p-2 mb-3">
      <i class="fas fa-star fs-5" v-for="i in 5"
         :class="{
            'text-warning': i <= modelValue ,
            'text-secondary': i > modelValue
         }"
         @click="$emit('update:modelValue', i)"
         role="button"
      ></i>
    </div>
  </div>

</template>

<script>
export default {
  name: "StarRating",
  props: {
    label: {
      type: String,
      required: true,
    },
    modelValue: {
      type: Number,
      required: true,
      default: 3,
    },
  }
}
</script>

<style scoped>

</style>