<template>
  <div class="shadow block p-0" style="overflow: auto">
    <table class="table table-striped table-borderless" style="min-width: 936px">
      <thead>
<!--      Заголовки -->
      <tr>
        <th v-for="header in headers">{{ header }}</th>
      </tr>

      </thead>
      <tbody>

<!--      Данные -->
      <tr v-for="row in data">

        <td v-for="column in row">
          <div v-if="typeof column != 'object'" v-html="column"></div>
          <div v-else>
            <RouterLink v-if="column.href" :to="column.href">{{ column.text }}</RouterLink>
            <Btn v-if="column.click" :class="column.cls" @click="column.click">{{ column.text }}</Btn>
          </div>
        </td>
      </tr>

<!--      Кнопка "Загрузить ещё" -->
      <tr v-if="!noLoadMore">
        <td :colspan="headers.length" class="text-center">
          <b @click="loadMore" class="text-primary" role="button">Загрузить ещё</b>
        </td>
      </tr>
      </tbody>
    </table>
  </div>

</template>

<script>
export default {
  name: "PageTable",
  props: {
    headers: {
      required: false,
    },
    data: {
      required: true,
    },
    noLoadMore: {
      required: false,
      default: false,
    }
  },

  methods: {
    loadMore(event) {
      this.$emit('loadMore');
    }
  }
}
</script>

<style scoped>

</style>