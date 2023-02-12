<template>
  <b v-if="showText" :class="`text-${(['danger', 'warning', 'success', 'secondary'])[status !== null ? status : 3]} d-flex align-items-center gap-2 my-3`">
    <div class="indicator" :class="`indicator-${(['danger', 'warning', 'success', 'secondary'])[status !== null ? status : 3]}`">
    </div>
    {{ (['не работает', 'работает медленно', 'работает', 'не проверялся'])[status !== null ? status : 3] }}
  </b>
  <div v-else class="indicator"
       :class="`indicator-${(['danger', 'warning', 'success', 'secondary'])[status !== null ? status : 3]}`">

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