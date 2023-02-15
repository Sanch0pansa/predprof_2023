<template>
  <Block>
    <div class="d-flex align-items-baseline justify-content-between mb-3">
      <div class="">
        <h3>{{ name }}</h3>
        <p class="text-muted mb-0">{{ url }} <a class="ms-2" target="_blank" :href="url"><i class="fas fa-external-link-alt text-primary"></i></a></p>
      </div>
      <div class="">
        <b class="text-primary">{{ added_by_user.username }}</b>
      </div>
    </div>

    <b class="d-block text-primary" role="button" @click="opened = !opened">{{ opened ? `Свернуть` : `Подробнее` }}</b>

    <div class="mt-3" v-if="opened">
      <p>{{ description }}</p>
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

  </Block>
</template>

<script>
export default {
  name: "ModerationPagesListItem",
  props: {
    name: {
      required: true,
      type: String,
    },
    description: {
      required: true,
      type: String,
    },
    url: {
      required: true,
      type: String,
    },
    id: {
      required: true,
      type: String,
    },
    added_by_user: {
      required: true,
      type: String,
    },
    status: {
      required: true,
      type: String
    }
  },
  data() {
    return {
      opened: false,
    }
  }
}
</script>

<style scoped>

</style>