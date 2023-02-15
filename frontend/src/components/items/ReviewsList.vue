<template>
  <ul class="reviews">
    <ReviewsListItem v-for="review in reviews"
                     :id="review.id"
                     :mark="review.mark"
                     :message="review.message"
                     :added_at="review.added_at"
                     :added_by_user__username="review.added_by_user__username"
                     :added_by_user="review.added_by_user"
    ></ReviewsListItem>
  </ul>
</template>

<script>
import ReviewsListItem from "@/components/items/ReviewsListItem.vue";

export default {
  name: "ReviewsList",
  components: {ReviewsListItem},
  props: {
    reviews: {
      required: true,
      type: Array
    }
  }
}
</script>

<style scoped>

</style>