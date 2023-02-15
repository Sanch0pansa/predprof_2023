<template>
  <ul class="reviews" v-if="loaded">
    <PersonalReportsListItem
        v-for="report in getReports()"
        :mark="report.mark"
        :message="report.message"
        :added_at="report.added_at"
        :page="report.page"
        :id="report.id"
        :status="report.status"
        @delete="sendRemovePersonalReport"
    ></PersonalReportsListItem>

    <li><b class="text-primary" v-if="reports.length > 3" role="button" @click="() => {opened = !opened}">{{ opened ? "Свернуть" : `Развернуть (eщё ${reports.length - 3})` }} </b></li>
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
      opened: false,
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
    },

    getReports() {
      if (this.opened) {
        return this.reports;
      } else {
        return this.reports.slice(0, 3);
      }
    }
  },
}
</script>

<style scoped>

</style>