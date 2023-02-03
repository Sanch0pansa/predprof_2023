<template>
  <b v-if="showText" :class="`text-${(['danger', 'warning', 'success', 'secondary'])[status]} d-flex align-items-center gap-2 my-3`">
    <div class="indicator" :class="`indicator-${(['danger', 'warning', 'success', 'secondary'])[status]}`">
    </div>
    {{ (['не работает', 'работает медленно', 'работает', 'не проверялся'])[status] }}
  </b>
  <div v-else class="indicator"
       :class="`indicator-${(['danger', 'warning', 'success', 'secondary'])[status]}`">

  </div>
</template>

<script>
export default {
  name: "Indicator",
  props: {
    status: {
      required: true,
      type: Number
    },
    showText: {
      required: false,
      default: false,
    }
  },
}
</script>

<style scoped>

</style>