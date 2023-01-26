<template>
  <PageSection :title="`Все ресурсы`">
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

export default {
  name: "PageChecks",
  components: {PageTable, RouterLink},
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
      const data = await this.getCheckingPages({first});

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
        this.pages.push([
            {text: page.name, href: {name: 'login'}},
            datetime.toLocaleString("ru", {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: "numeric",
              minute: "numeric",
              second: "numeric"
            }).replaceAll(" г", "").replaceAll(".", ""),
            `<b class="text-${statesColors[page.check_status]}">${statesNames[page.check_status]}</b>`,
            `<b class="text-${statesColors[page.check_status]}">${page.last_check_timeout}</b>`,
            100,
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