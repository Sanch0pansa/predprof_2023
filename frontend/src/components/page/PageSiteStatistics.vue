<template>
  <PageSection :title="`Статистика`">
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
            <th>{{ failures }}</th>
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
        <i class="fas fa-chart-pie text-primary" style="font-size: 120px;"></i>
      </div>
    </div>

  </Block>
  </PageSection>
</template>

<script>
import {mapActions} from "vuex";

export default {
  name: "PageSiteStatistics",
  data() {
    return {
      pages: 0,
      failures: 0,
      reports: 0,
      reviews: 0,
    }
  },

  methods: {
    ...mapActions({
      getStatistics: "pages/getStatistics"
    }),

    async fetchStatistics() {
      const data = await this.getStatistics();


      this.pages = data.total_pages;
      this.failures = data.detected_failures;
      this.reports = data.total_reports;
      this.reviews = data.total_reviews;

    }
  },

  async mounted() {
    await this.fetchStatistics();

  }
}
</script>

<style scoped>

</style>