<template>
  <PageSection :title="`Все ресурсы`">
    <Block class="mb-2 d-flex align-items-end">
      <Inp v-model="search" label="Поиск по сайтам" class="w-100 me-3"></Inp>
      <Btn @click="fetchCheckingPages">Искать</Btn>
    </Block>

    <PageTable
        :headers="['Сайт', 'Последняя проверка', 'Состояние', 'Задержка ответа, мс', 'Рейтинг']"
        :data="pages"
        :no-load-more="!this.$store.state.pages.canLoadMore"
        @loadMore="loadMore"
    ></PageTable>
  </PageSection>
</template>

<script>
import PageTable from "@/components/page/PageTable.vue";
import {mapActions, mapState} from "vuex";
import {RouterLink} from "vue-router";
import Block from "@/components/UI/Block.vue";

export default {
  name: "PageChecks",
  components: {Block, PageTable, RouterLink},
  data() {
    return {
      headers: [
        'Сайт',
        'Последняя проверка',
        'Состояние',
        'Задержка ответа, мс',
        'Рейтинг'
      ],
      pages: [],
      search: "",
    }
  },

  methods: {
    ...mapActions({
      getCheckingPages: "pages/getCheckingPages",
    }),

    loadMore() {
      this.fetchCheckingPages();
    },

    async fetchCheckingPages(first=false) {
      if (this.search) {
        this.pages = [];
      }
      const data = await this.getCheckingPages({first: first || this.search, search: this.search});

      const statesNames = [
          "Не работает",
          "Работает медленно",
          "Работает",
          "Не проверялся"
      ];

      const statesColors = [
          "danger",
          "warning",
          "success",
          "secondary"
      ];

      data.forEach(page => {
        let datetime = new Date(page.last_check_time);
        let status = page.check_status;
        let time = page.last_check_time ? datetime.toLocaleString("ru", {
          year: 'numeric',
          month: 'short',
          day: 'numeric',
          hour: "numeric",
          minute: "numeric",
          second: "numeric"
        }).replaceAll(" г", "").replaceAll(".", "") : '-';
        let timeout = page.last_check_timeout ? page.last_check_timeout : '-';
        if (status == null) {
          status = 3;
        }
        this.pages.push([
            {text: page.name, href: {name: 'single_page', params: {id: page.id}}},
            time,
            `<b class="text-${statesColors[status]}">${statesNames[status]}</b>`,
            `<b class="text-${statesColors[status]}">${timeout}</b>`,
            `<i class="fas fa-star text-warning"></i> ${Number(page.rating)}`,
        ]);
      });
    }
  },

  async mounted() {
    await this.fetchCheckingPages(true);
  }
}
</script>

<style scoped>

</style>