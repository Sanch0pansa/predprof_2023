<template>
  <div class="row pt-5">
    <div class="col-md-5">
        <h1>{{ name }}</h1>
        <h3>{{ url }}</h3>
        <b class="text-success d-flex align-items-center gap-2 my-3">
          <Indicator :status="status" :show-text="true"></Indicator>
        </b>
        <p>{{ description }}</p>
        <div class="d-flex gap-3 align-items-center flex-wrap mb-3">
          <Link :href="`${url}`" target="_blank">Перейти на сайт</Link>
          <Btn v-if="!subscribed" @click="subscribe">Отслеживать состояние</Btn>
          <Btn v-else @click="unsubscribe" :class="`btn-secondary`">Прекратить отслеживать</Btn>
        </div>
        <Btn class="btn-warning" v-if="getIsModerator()" @click="sendPageModeration">Отправить на модерацию</Btn>
        <br>

    </div>
    <div class="col-md-1"></div>
    <div class="col-md-6">
      <Block>
        <div class="d-flex justify-content-between align-items-center">
          <span>Состояние</span>
          <b class="text-end" v-html="lastCheck.check_status"></b>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
          <span>Время задержки, мс</span>
          <b class="text-end" v-html="lastCheck.response_time"></b>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
          <span>Последняя проверка</span>
          <span class="text-end">{{ lastCheck.checked_at }}</span>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
          <span>Всего проверок</span>
          <span class="text-end">{{ checks.length }}</span>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
          <span>Отзывов</span>
          <span class="text-end">{{ reviews.length }}</span>
        </div>
        <div class="d-flex justify-content-between align-items-center mt-3">
          <span>Рейтинг</span>
          <span class="text-end"><i class="fas fa-star text-warning"></i> {{ rating }}</span>
        </div>
        <br>
        <RouterLink :to="`/checker/?url=${url}`" class="btn btn-primary" >Отчёт по сайту</RouterLink>
      </Block>
    </div>
  </div>
  <PageSection :title="`График задержки ответа`">
    <Block>
      <Line v-if="chart.loaded"
          id="my-chart-id"
          :options="chart.chartOptions"
          :data="chart.chartData"
          :style="`max-height: 400px`"
      />
    </Block>
  </PageSection>
  <PageSection :title="`Последние проверки`">
    <PageTable
        :data="checksForTable"
        :headers="['Время проверки', 'Состояние', 'Задержка ответа, мс']"
        @loadMore="loadMore"
        :no-load-more="checksForTable.length >= checks.length"
    ></PageTable>
  </PageSection>
  <PageSection :title="`Сообщение о сбоях`">
    <ModalBtn :class="`mb-3`" id="creatingReportModal">Сообщить о сбое</ModalBtn>
    <PageTable
        v-if="reportsForTable.length"
        :data="reportsForTable"
        :headers="reportsTableHeaders"
        :no-load-more="true"
    ></PageTable>
    <div class="text-muted" v-else>Сообщений о сбоях не было</div>
  </PageSection>
  <PageSection :title="`Отзывы`">
    <ModalBtn :class="`mb-3`" id="creatingReviewModal">Добавить отзыв</ModalBtn>
    <ReviewsList v-if="reviews.length" :reviews="reviews"></ReviewsList>
    <div class="text-muted" v-else>Отзывов нет</div>
  </PageSection>

  <Modal id="creatingReportModal" :title="`Добавление сообщения о сбое`">
    <CreatingReportForm :id="$route.params.id">

    </CreatingReportForm>
  </Modal>

  <Modal id="creatingReviewModal" :title="`Добавление отзыва`">
    <CreatingReviewForm :id="$route.params.id">

    </CreatingReviewForm>
  </Modal>
</template>

<script>
import Link from "@/components/UI/Link.vue";
import PageSection from "@/components/UI/Section.vue";
import { Line } from 'vue-chartjs'
import {Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import PageTable from "@/components/page/PageTable.vue";
import {mapActions, mapGetters, mapState} from "vuex";
import ReviewsList from "@/components/items/ReviewsList.vue";
import Indicator from "@/components/UI/Indicator.vue";
import Modal from "@/components/UI/Modal.vue";
import ModalBtn from "@/components/UI/ModalBtn.vue";
import CreatingReportForm from "@/components/forms/CreatingReportForm.vue";
import CreatingReviewForm from "@/components/forms/CreatingReviewForm.vue";

ChartJS.register(CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    Filler
)


export default {
  name: "SinglePageView",
  components: {
    CreatingReviewForm,
    CreatingReportForm, ModalBtn, Modal, Indicator, ReviewsList, PageTable, PageSection, Link, Line},
  data() {
    return {
      name: "",
      url: "",
      description: "",
      status: 2,
      rating: 0,
      subscribed: false,
      lastCheck: {
        check_status: 3,
        response_time: 0,
        checked_at: ""
      },
      chart: {
        loaded: false,
        chartData: {
          labels: [],
          datasets: [
            {
              data: [],
              backgroundColor: "rgba(58,133,246,0.29)",
              borderColor: "#3A85F6",
              label: "Задержка ответа, мс",
              fill: "start"
            },
          ]
        },
        chartOptions: {
          responsive: true,
          plugins: {
            filler: {},
          },
          interaction: {
            intersect: false,
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        },
      },
      checks: [],
      reports: [],
      reviews: [],

      checksForTable: [],
      reportsForTable: [],
      reportsTableHeaders: ['Время сообщения', 'Подробности', 'Пользователь'],
    }
  },

  methods: {
    ...mapActions({
      getPageData: "pages/getPageData",
      subscribePage: "pages/subscribePage",
      unsubscribePage: "pages/unsubscribePage",
      getPageSubscription: "pages/getPageSubscription",
      patchPageStatus: "moderation/patchPageStatus",
      patchReportStatus: "moderation/patchReportStatus",
    }),

    ...mapGetters({
      getIsModerator: "auth/getIsModerator",
    }),

    async sendPageModeration() {
      await this.patchPageStatus({id: this.$route.params.id, action: "revise"});
      this.$router.replace({name: 'moderation_pages'});
    },

    async subscribe() {
      let res = await this.subscribePage({id: this.$route.params.id});

      if (res.success) {
        this.subscribed = true;
      }
    },

    async unsubscribe() {
      let res = await this.unsubscribePage({id: this.$route.params.id});

      if (res.success) {
        this.subscribed = false;
      }
    },

    async getSubscription() {
      let res = await this.getPageSubscription({id: this.$route.params.id});

      if (res.subscribed) {
        this.subscribed = true;
      }
    },

    loadMore() {
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
      let ln = this.checksForTable.length;
      [...this.checks].reverse().slice(ln, ln + 10).forEach(check => {
        let checkRow = [
          (new Date(check.checked_at)).toLocaleString("ru", {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: "numeric",
            minute: "numeric",
            second: "numeric"
          }).replaceAll(" г", "").replaceAll(".", ""),
          `<b class="text-${statesColors[check.check_status]}">${statesNames[check.check_status]}</b>`,
          `<b class="text-${statesColors[check.check_status]}">${check.response_time}</b>`,
        ];

        this.checksForTable.push(checkRow);
      })
    },

    async fetchPageData() {
      let data = await this.getPageData({id: this.$route.params.id});
      await this.getSubscription();

      this.name = data.data.name;
      this.url = data.data.url;
      this.description = data.data.description;
      this.status = data.data.status;
      this.rating = data.data.rating;

      this.chart.chartData.labels = [];
      this.chart.chartData.datasets[0].data = [];

      data.checks.forEach(check => {
        this.chart.chartData.labels.push(
            (new Date(check.checked_at)).toLocaleString("ru", {
              year: 'numeric',
              month: 'short',
              day: 'numeric',
              hour: "numeric",
              minute: "numeric",
              second: "numeric"
            })
        );

        this.chart.chartData.datasets[0].data.push(
            check.response_time
        );
      });

      this.reports = data.reports;
      this.checks = data.checks;
      this.reviews = data.reviews;

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

      this.checksForTable = [];
      let lastCheckDefined = false;
      [...this.checks].reverse().slice(0, 3).forEach(check => {
        let checkRow = [
          (new Date(check.checked_at)).toLocaleString("ru", {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: "numeric",
            minute: "numeric",
            second: "numeric"
          }).replaceAll(" г", "").replaceAll(".", ""),
          `<b class="text-${statesColors[check.check_status]}">${statesNames[check.check_status]}</b>`,
          `<b class="text-${statesColors[check.check_status]}">${check.response_time}</b>`,
        ];

        this.checksForTable.push(checkRow);

        if (!lastCheckDefined) {
            this.lastCheck = {
              response_time: checkRow[2],
              checked_at: checkRow[0],
              check_status: checkRow[1]
            }
            lastCheckDefined = true;
        }

      })

      if (this.getIsModerator()) {
        this.reportsTableHeaders = ['Время сообщения', 'Подробности', 'Пользователь', 'Действия'];
      }

      this.reportsForTable = [];
      this.reports.forEach(report => {
        let reportRow = [
          (new Date(report.added_at)).toLocaleString("ru", {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: "numeric",
            minute: "numeric",
            second: "numeric"
          }),
          report.message,
          {username: report.added_by_user__username, id: report.added_by_user}
        ];

        if (this.getIsModerator()) {
          reportRow.push({text: 'Отправить на модерацию', click: async () => {
            await this.patchReportStatus({id: report.id, action: 'revise'});
            this.$router.replace({name: 'moderation_reports'});
            }, cls: "btn-warning"});
        }

        this.reportsForTable.push(reportRow);
      });

      this.chart.loaded = true;
    },
  },

  async mounted() {
    await this.fetchPageData();
  }
}
</script>

<style scoped>

</style>