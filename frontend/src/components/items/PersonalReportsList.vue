<template>
  <ul class="reviews" v-if="loaded">
    <PersonalReportsListItem
        v-for="report in reports"
        :mark="report.mark"
        :message="report.message"
        :added_at="report.added_at"
        :page="report.page"
        :id="report.id"
        :status="report.status"
        @delete="sendRemovePersonalReport"
    ></PersonalReportsListItem>
  </ul>
  <Btn v-else @click="fetchPersonalReports">Показать</Btn>
</template>

<script>
import PersonalReportsListItem from "@/components/items/PersonalReportsListItem.vue";
import {mapActions} from "vuex";
import Btn from "@/components/UI/Btn.vue";

export default {
  name: "PersonalReportsList",
  components: {Btn, PersonalReportsListItem},
  data() {
    return {
      reports: [],
      loaded: false,
    }
  },
  methods: {
    ...mapActions({
      getPersonalReports: "reports/getPersonalReports",
      removePersonalReport: "reports/removePersonalReport",
    }),

    async fetchPersonalReports() {
      this.reports = await this.getPersonalReports();
      this.loaded = true;
    },

    async sendRemovePersonalReport(id) {
      await this.removePersonalReport({id: id});
    }
  },
}
</script>

<style scoped>

</style>