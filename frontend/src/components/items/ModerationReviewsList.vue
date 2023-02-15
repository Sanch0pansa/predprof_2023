<template>
  <Tabs :tabs="['Нерасмотренные', 'Отклонённые']">
    <template #tab0>
      <ul class="reviews">
        <ModerationReviewsListItem
            v-for="review in reviews.moderation"
            :mark="review.mark"
            :message="review.message"
            :added_at="review.added_at"
            :added_by_user="review.added_by_user"
            :page="review.page"
            :id="review.id"
            status="moderation"
            @action="action"
        ></ModerationReviewsListItem>
      </ul>
    </template>
    <template #tab1>
      <ul class="reviews">
        <ModerationReviewsListItem
            v-for="review in reviews.rejected"
            :mark="review.mark"
            :message="review.message"
            :added_at="review.added_at"
            :added_by_user="review.added_by_user"
            :page="review.page"
            :id="review.id"
            status="rejected"
            @action="action"
        ></ModerationReviewsListItem>
      </ul>
    </template>
  </Tabs>
</template>

<script>
import ModerationReviewsListItem from "@/components/items/ModerationReviewsListItem.vue";
import Tabs from "@/components/UI/Tabs.vue";

export default {
  name: "ModerationReviewsList",
  components: {ModerationReviewsListItem, Tabs},
  props: {
    reviews: {
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