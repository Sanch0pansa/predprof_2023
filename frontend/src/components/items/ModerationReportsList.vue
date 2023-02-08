<template>
  <Tabs :tabs="['Нерасмотренные', 'Отклонённые']">
    <template #tab0>
      <ul class="reviews">
        <ModerationReportsListItem
            v-for="report in reports.moderation"
            :message="report.message"
            :added_at="report.added_at"
            :added_by_user="report.added_by_user"
            :page="report.page"
            :id="report.id"
            status="moderation"
            @action="action"
        ></ModerationReportsListItem>
      </ul>
    </template>
    <template #tab1>
      <ul class="reviews">
        <ModerationReportsListItem
            v-for="report in reports.rejected"
            :message="report.message"
            :added_at="report.added_at"
            :added_by_user="report.added_by_user"
            :page="report.page"
            :id="report.id"
            status="rejected"
            @action="action"
        ></ModerationReportsListItem>
      </ul>
    </template>
  </Tabs>
</template>

<script>
import Tabs from "@/components/UI/Tabs.vue";
import ModerationReportsListItem from "@/components/items/ModerationReportsListItem.vue";

export default {
  name: "ModerationReportsList",
  components: {ModerationReportsListItem, Tabs},
  props: {
    reports: {
      required: true,
      type: Array
    }
  },
  methods: {
    async action(data) {
      await this.$emit("action", data);
    }
  },
}
</script>

<style scoped>

</style>