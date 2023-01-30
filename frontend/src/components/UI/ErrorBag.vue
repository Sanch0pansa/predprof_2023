<template>
  <div class="mt-2" v-if="errors.length || success">
    <div class="alert alert-danger text-start alert-dismissible" role="alert" v-for="(error, number) in errors" :key="number">
      {{ error }}
      <button type="button" class="btn-close" aria-label="Close" @click="deleteError(number)"></button>
    </div>

    <div class="alert alert-success text-start alert-dismissible" role="alert" v-if="success != ''">
      {{ success }}
      <button type="button" class="btn-close" aria-label="Close" @click="deleteSuccess"></button>
    </div>
  </div>

</template>

<script>
export default {
  name: "ErrorBag",
  props: {
    errors: {
      type: Array,
      required: false,
      default: []
    },
    success: {
      type: String,
      required: false,
      default: ""
    },
  },
  methods: {
    deleteError(n) {
      this.$emit('update:errors', this.errors.filter((el, i) => i != n));
    },
    deleteSuccess(n) {
      this.$emit('update:success', "");
    },
  }
}
</script>

<style scoped>

</style>