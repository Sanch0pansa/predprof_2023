<template>
  <PageWelcomeSection></PageWelcomeSection>
  <div class="row">
    <div class="col-lg-6">
      <PageSection :title="`Популярные ресурсы`">
        <PagesList></PagesList>
      </PageSection>
    </div>
    <div class="col-lg-6">
      <PageSection :title="`Статистика`">
        <PageSiteStatistics>

        </PageSiteStatistics>
      </PageSection>
    </div>
    <div class="col-12">
      <PageSection :title="`Таблица`">
        <PageTable
            :headers="['Сайт', 'Последняя проверка', 'Состояние', 'Задержка ответа, мс', 'Рейтинг']"
            :data="tableData"
            :noLoadMore="true"

            @loadMore="loadMore"
        ></PageTable>
      </PageSection>
    </div>
  </div>
</template>

<script>
import PageHeader from "@/components/page/PageHeader.vue";
import PageFooter from "@/components/page/PageFooter.vue";
import PageTable from "@/components/page/PageTable.vue";
import PageWelcomeSection from "@/components/page/PageWelcomeSection.vue";
import PagesList from "@/components/items/PagesList.vue";
import PageSiteStatistics from "@/components/page/PageSiteStatistics.vue";

export default {
  name: "HomeView",
  components: {PageHeader, PageFooter, PageTable, PageWelcomeSection, PagesList, PageSiteStatistics},
  data() {
    return {
      tableData: [
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
        [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '100'],
      ]
    }
  },
  methods: {
    loadMore() {
      this.tableData.push(
          [`<a href='https://google.com'>google.com</a>`, '22 янв 2023, 23:04:45', `<b class='text-success'>Работает</b>`, `<b class='text-success'>26</b>`, '99'],
      );
    }
  }
}
</script>

<style scoped>

</style>