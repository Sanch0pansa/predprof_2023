<template>
  <li class="review">
    <div class="review-header">
      <Link :href="`https://google.com`">{{ added_by_user__username }}</Link>
      <div class="text-muted">{{ (new Date(added_at)).toLocaleDateString("ru", {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      }) }}</div>
    </div>
    <div class="review-mark">
      <i class="fas fa-star"></i>
      <b>{{ mark }}</b>
    </div>
    <div class="review-content">
      <p>{{ message }}</p>
    </div>
  </li>
</template>

<script>
export default {
  name: "ReviewsListItem",
  props: {
    added_by_user: {
      required: true,
      type: Number
    },
    added_by_user__username: {
      required: true,
      type: String
    },
    added_at: {
      required: true,
      type: String
    },
    message: {
      required: true,
      type: String
    },
    mark: {
      required: true,
      type: Number
    }
  }
}
</script>

<style scoped>

</style>