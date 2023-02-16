<template>
  <div class="row pt-5">
    <PageBreadcrumbs :links-names="['moderation', 'moderation_reports']"></PageBreadcrumbs>
    <div class="col-12">
      <h1>Модерация сообщений о сбоях</h1>
    </div>
    <div class="col-12 mt-5 d-flex flex-column gap-3">
      <ModerationReportsList :reports="reports" @action="sendPatchReportStatus"></ModerationReportsList>
    </div>
  </div>
</template>

<script>
import {mapActions} from "vuex";
import ModerationReportsList from "@/components/items/ModerationReportsList.vue";
import PageBreadcrumbs from "@/components/page/PageBreadcrumbs.vue";

export default {
  name: "ModerationReportsView",
  components: {PageBreadcrumbs, ModerationReportsList},
  data() {
    return {
      reports: {
        moderation: [

        ],
        rejected: [

        ]
      }
    }
  },
  methods: {
    ...mapActions({
      getModerationReports: "moderation/getModerationReports",
      getRejectedReports: "moderation/getRejectedReports",
      patchReportStatus: "moderation/patchReportStatus",
    }),
    async fetchReports() {
      this.reports.moderation = await this.getModerationReports();
      this.reports.rejected = await this.getRejectedReports();
    },

    async sendPatchReportStatus({id, action}) {
      let res = await this.patchReportStatus({
        id: id,
        action: action
      });

      if (res.success) {
        await this.fetchReports();
      }
    }
  },
  async mounted() {
    await this.fetchReports();
  }
}
</script>

<style scoped>

</style>