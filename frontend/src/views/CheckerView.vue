<template>
  <div class="row pt-5">
    <div class="col-12">
      <Block>
        <h1>Проверьте Ваш сайт:</h1>
        <Inp label="URL сайта" name="url" v-model="url" class="form-control-lg ps-0 mt-3"></Inp>
        <Btn @click="check" class="btn-lg mt-3">Получить отчёт о доступности</Btn>

      </Block>
    </div>
    <div class="col-12 mt-4" v-if="first_step.loading_status > 0">
      <Block>
        <template v-if="first_step.loading_status == 1">
          <h2>Идёт проверка сайта на базовом уровне... </h2>
          <div class="d-grid" style="place-items: center; height: 200px">
            <div class="spinner-border text-success" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>


        </template>
        <template v-if="first_step.loading_status == 2">
          <h2>Основные результаты</h2>
          <table class="table table-striped mt-4">
            <tbody>
              <tr>
                <th>Пинг сервера, мс</th>
                <td>{{ first_step.ping }}</td>
              </tr>
              <tr>
                <th>Задержка ответа, мс</th>
                <td>{{ first_step.response_time }}</td>
              </tr>
              <tr>
                <th>Ответ</th>
                <td>{{ first_step.response_status_code }}</td>
              </tr>
              <tr>
                <th>Вердикт</th>
                <td>{{ first_step.response_status_code == 200 ? "Сайт доступен" : "Сайт не доступен" }}</td>
              </tr>
            </tbody>
          </table>
        </template>
        <template v-if="first_step.loading_status == 3">
          <h2>Не удалось проверить (</h2>
          <table class="table table-striped mt-4">
            <tbody>
            <tr>
              <th>Пинг сервера, мс</th>
              <td>{{ first_step.ping }}</td>
            </tr>
            <tr>
              <th>Задержка ответа, мс</th>
              <td>{{ first_step.response_time }}</td>
            </tr>
            <tr>
              <th>Ответ</th>
              <td>{{ first_step.response_status_code }}</td>
            </tr>
            <tr>
              <th>Вердикт</th>
              <td>{{ first_step.response_status_code == 200 ? "Сайт доступен" : "Сайт не доступен" }}</td>
            </tr>
            </tbody>
          </table>
        </template>

      </Block>
    </div>

    <div class="col-12 mt-4" v-if="second_step.loading_status > 0">
      <Block>
        <template v-if="second_step.loading_status == 1">
          <h2>Идёт проверка сайта средствами Google PageSpeed Insights... </h2>
          <div class="d-grid" style="place-items: center; height: 200px">
            <div class="spinner-border text-success" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </template>
        <template v-if="second_step.loading_status == 2">
          <h2>Результаты Google PageSpeed Insights</h2>
          <table class="table table-striped mt-4">
            <tbody>
            <tr>
              <th>Время загрузки первого контента, мс</th>
              <td>{{ second_step.first_contentful_paint }}</td>
            </tr>
            <tr>
              <th>Время загрузки первой значащей части контента, мс</th>
              <td>{{ second_step.first_meaningful_paint }}</td>
            </tr>
            <tr>
              <th>Время загрузки самой большой части контента, мс</th>
              <td>{{ second_step.largest_contentful_paint }}</td>
            </tr>
            <tr>
              <th>Индекс скорости, мс</th>
              <td>{{ second_step.speed_index }}</td>
            </tr>
            <tr>
              <th>Время полной загрузки страницы, мс</th>
              <td>{{ second_step.full_page_loading_time }}</td>
            </tr>
            <tr>
              <th>Оценка Google PageSpeed Insights</th>
              <td><span :class="`badge bg-${second_step.score < 50 ? 'danger' : (second_step.score < 90 ? 'warning' : 'success')} fs-4`">{{ second_step.score }}</span></td>
            </tr>
            </tbody>
          </table>
        </template>
        <template v-if="second_step.loading_status == 3">
          <h2>Не удалось проверить средствами Google PageSpeed Insights</h2>
        </template>
      </Block>
    </div>
    <div class="col-12 mt-4" v-if="third_step.loading_status > 0">
      <Block>
        <template v-if="third_step.loading_status == 1">
          <h2>Формирование документа</h2>
          <template v-if="has_data">
            <h5 class="my-4">В базе найдены данные об этом ресурсе. Укажите период, данные за который Вы хотите добавить в документ.</h5>
            <div class="row mb-4">
              <div class="col-6">
                <Inp label="Начало периода" type="date" name="date_from" v-model="date_from"></Inp>
              </div>
              <div class="col-6">
                <Inp label="Конец периода" type="date" name="date_to" v-model="date_to"></Inp>
              </div>
            </div>
          </template>
          <template v-else>
            <h5 class="my-4">В базе не найдены данные об этом ресурсе. Документ будет сформирован на основе проведенной проверки.</h5>
          </template>
          <Btn @click="makeDocument">Сформировать документ</Btn>
        </template>
        <template v-if="third_step.loading_status == 2">
          <h2>Формирование документа...</h2>
          <div class="d-grid" style="place-items: center; height: 200px">
            <div class="spinner-border text-success" role="status">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        </template>
        <template v-if="third_step.loading_status == 3">
          <h2>Документ сформирован</h2>
          <a class="btn btn-primary mt-3 text-light" :href="third_step.document_url" target="_blank"><i class="fas fa-file-excel text-light"></i> Скачать</a>
          <template v-if="third_step.other_check_reports.length">
              <h5 class="mt-4">Найдены другие отчёты по этой странице:</h5>
              <ul>
                <li v-for="check_report in third_step.other_check_reports"><a :href="check_report.document_url" target="_blank">{{ check_report.date }}</a></li>
              </ul>
          </template>
        </template>
      </Block>
    </div>
  </div>
</template>
<script>
import Inp from "@/components/UI/Inp.vue";
import {mapActions} from "vuex";
import Btn from "@/components/UI/Btn.vue";

export default {
  name: "CheckerView",
  components: {Btn, Inp},
  data() {
    let date = new Date();
    let dateTime = (new Date(date.getTime() - (date.getTimezoneOffset() * 60000))).toISOString();
    return {
      url: this.$route.query.url,
      report_id: 0,
      checking: false,
      error: false,
      has_data: false,
      date_from: dateTime.split('T')[0],
      date_to: dateTime.split('T')[0],
      first_step: {
        loading_status: 0,
        ping: 0.012,
        response_status_code: 200, // Код ответа
        response_time: 0.034, // Задержка ответа
      },
      second_step: {
        loading_status: 0,
        first_contentful_paint: 0,
        first_meaningful_paint: 0,
        largest_contentful_paint: 0,
        speed_index: 0,
        full_page_loading_time: 0,
        score: 0,
      },
      third_step: {
        loading_status: 0,
        document_url: "https://google.com",
        other_check_reports: [],
      }
    }
  },
  async mounted() {
    if (this.$route.query.url) {
      await this.check();
    }
  },
  methods: {

    ...mapActions({
      getFirstRequest: "deepCheck/getFirstRequest",
      getSecondRequest: "deepCheck/getSecondRequest",
      getThirdRequest: "deepCheck/getThirdRequest",
    }),

    async check() {
      if (this.checking) {
        return true;
      }

      this.checking = true;

      // Проверка на базовом уровне
      this.first_step.loading_status = 1;
      let res = await this.getFirstRequest({url: this.url});

      if (res.id) {
        this.first_step.ping = res.ping;
        this.first_step.response_time = res.response_time;
        this.first_step.response_status_code = res.response_status_code;
        this.has_data = res.has_data;
        this.report_id = res.id;

        this.first_step.loading_status = 2;

      } else {

        this.first_step.loading_status = 3;

        return true;
      }

      // Проверка средствами Google Page Speed Insights
      this.second_step.loading_status = 1;
      res = await this.getSecondRequest({id: this.report_id});
      console.log(res);

      if (res.score !== undefined) {
        this.second_step.first_contentful_paint = res.first_contentful_paint;
        this.second_step.first_meaningful_paint = res.first_meaningful_paint;
        this.second_step.largest_contentful_paint = res.largest_contentful_paint;
        this.second_step.speed_index = res.speed_index;
        this.second_step.score = res.score;
        this.second_step.full_page_loading_time = res.full_page_loading_time;

        this.second_step.loading_status = 2;

      } else {

        this.second_step.loading_status = 3;

        return true;
      }

      this.third_step.loading_status = 1;
    },

    async makeDocument() {
      this.third_step.loading_status = 2;

      let res = await this.getThirdRequest({
        id: this.report_id,
        date_from: this.date_from + "T00:00:00.000+03:00",
        date_to: this.date_to + "T23:59:59.000+03:00",
      });

      this.third_step.document_url = res.document_url;
      this.third_step.loading_status = 3;
      this.third_step.other_check_reports = res.other_check_reports;
    }
  }
}
</script>

<style scoped>

</style>