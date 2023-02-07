<template>
  <Tabs :tabs="['Нерасмотренные', 'Отклонённые']">
    <template #tab0>
      <div class="d-flex flex-column gap-3">
        <ModerationPagesListItem
            :id="page.id"
            :user="page.user"
            :url="page.url"
            :description="page.description"
            :name="page.name"
            status="moderation"
            @action="action"
            v-for="page in pages.moderation">

        </ModerationPagesListItem>
      </div>
    </template>
    <template #tab1>
      <div class="d-flex flex-column gap-3">
        <ModerationPagesListItem
            :id="page.id"
            :user="page.user"
            :url="page.url"
            :description="page.description"
            :name="page.name"
            status="rejected"
            @action="action"
            v-for="page in pages.rejected">

        </ModerationPagesListItem>
      </div>
    </template>
  </Tabs>
</template>

<script>
import ModerationPagesListItem from "@/components/items/ModerationPagesListItem.vue";

export default {
  name: "ModerationPagesList",
  components: {ModerationPagesListItem},
  props: {
    pages: {
      required: true,
      type: Object,
    }
  },
  methods: {
    async action(data) {
      await this.$emit("action", data);
    }
  }
}
</script>

<style scoped>

</style>