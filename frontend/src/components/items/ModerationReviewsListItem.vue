<template>
  <li class="review">
    <div class="review-header">
      <Username :username="added_by_user.username" :id="added_by_user.id"></Username>
      <br>
      Сайт: <RouterLink :to="{name: 'single_page', params: {id: page.id}}">{{ page.name }}</RouterLink>
      <div class="text-muted">{{ (new Date(added_at)).toLocaleDateString("ru", {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      }) }}</div>
    </div>
    <div class="review-mark">
      <i class="fas fa-star fs-5" v-for="i in 5"
         :class="{
            'text-warning': i <= mark ,
            'text-secondary': i > mark
         }"
      ></i>
    </div>

    <b class="d-block text-primary" role="button" @click="opened = !opened">{{ opened ? `Свернуть` : `Подробнее` }}</b>

    <div v-if="opened" class="review-content">
      <p class="my-3">{{ message }}</p>
      <div class="d-flex flex-wrap gap-2" v-if="status === 'moderation'">
        <Btn class="btn-success" @click="$emit('action', {id: id, action: 'accept'})">Одобрить</Btn>
        <Btn class="btn-warning" @click="$emit('action', {id: id, action: 'reject'})">Отклонить</Btn>
        <Btn class="btn-danger" @click="$emit('action', {id: id, action: 'delete'})">Удалить</Btn>
      </div>
      <div class="d-flex flex-wrap gap-2" v-else>
        <Btn class="btn-primary" @click="$emit('action', {id: id, action: 'revise'})">Пересмотреть</Btn>
        <Btn class="btn-danger" @click="$emit('action', {id: id, action: 'delete'})">Удалить</Btn>
      </div>
    </div>
  </li>
</template>

<script>
export default {
  name: "ModerationReviewsListItem",
  props: {
    added_by_user: {
      required: true,
      type: Object
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
    },
    status: {
      type: String,
      required: true,
    },
    id: {
      type: Number,
      required: true,
    },
    page: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      opened: false,
    }
  },
}
</script>

<style scoped>

</style>