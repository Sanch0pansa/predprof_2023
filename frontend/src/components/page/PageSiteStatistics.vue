<template>
  <Block>
    <div class="row">
      <div class="col-7">
        <table class="fs-5 w-100 table-big">
          <tr>
            <td>Сайтов в реестре:</td>
            <th>{{ pages }}</th>
          </tr>
          <tr>
            <td>Выявлено сбоев:</td>
            <th>{{ malfunctions }}</th>
          </tr>
          <tr>
            <td>Сообщений о сбоях:</td>
            <th>{{ reports }}</th>
          </tr>
          <tr>
            <td>Отзывов о сайтах:</td>
            <th>{{ reviews }}</th>
          </tr>
        </table>
      </div>
      <div class="col-5 d-grid" style="place-items: center">
        <i class="fa-solid fa-chart-pie text-primary" style="font-size: 120px;"></i>
      </div>
    </div>

  </Block>
</template>

<script>
export default {
  name: "PageSiteStatistics",
  data() {
    return {
      pages: 0,
      malfunctions: 0,
      reports: 0,
      reviews: 0,
    }
  },
  async mounted() {
    // Здесь будет запрос на получение статистики
    this.pages = 2623;
    this.malfunctions = 45;
    this.reports = 156;
    this.reviews = 608;
  }
}
</script>

<style scoped>

</style>