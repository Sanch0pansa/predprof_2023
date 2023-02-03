<template>
<Btn data-bs-toggle="modal" :data-bs-target="`#${id}`">
  <slot></slot>
</Btn>
</template>

<script>
export default {
  name: "ModalBtn",
  props: {
    id: {
      type: Number,
      required: true,
    }
  }
}
</script>

<style scoped>

</style>