<template>
  <li class="list-group-item card-body py-3">
    <p class="fw-bold card-title mb-2"><span style="width: 30px;" :class="`badge bg-${typesToColors[data.type]}`"><i :class="`text-light fas ${typesToIcons[data.type]}`"></i></span> <span class="text-primary"><RouterLink :to="{name: 'single_page', params: {id: data.page.id}}">{{ data.page.name }}</RouterLink></span></p>
    <template v-if="data.type === 'failure'">
      Зафиксирован сбой в работе ресурса.<br>При запросе автоматической системой возникает <b class="text-danger">{{ data.detail.error_description }}</b>.<br>
      Возможные причины:<br>
      <ul>
        <li v-for="reason in data.detail.reasons">{{ reason }}</li>
      </ul>
    </template>
    <template v-if="data.type === 'lazy_loading'">
      Зафиксирована задержка ответа ресурса.<br>При запросе автоматической системой продолжительность задержки составляла <b class="text-warning">{{ data.detail.time }}</b> мс.<br>
      Возможные причины:<br>
      <ul>
        <li v-for="reason in data.detail.reasons">{{ reason }}</li>
      </ul>
    </template>
    <template v-if="data.type === 'report'">
      Пользователь <Username :id="data.detail.user.id" :username="data.detail.user.username"></Username> сообщил о сбое в работе ресурса:<br>
      <i class="d-block m-3">
        {{ data.detail.message }}
      </i>
    </template>
    <template v-if="data.type === 'review'">
      Пользователь <Username :id="data.detail.user.id" :username="data.detail.user.username"></Username> поставил ресурсу <b>{{ data.detail.mark }}</b><i class="text-warning fas fa-star"></i> и оставил отзыв:<br>
      <i class="d-block m-3">
        {{ data.detail.message }}
      </i>
    </template>
    <span class="mt-1 d-block text-muted">{{ (new Date(data.message_datetime)).toLocaleString("ru", {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: "numeric",
      minute: "numeric",
      second: "numeric"
    }) }}</span>

  </li>
</template>

<script>
import Username from "@/components/UI/Username.vue";

export default {
  name: "EventsListItem",
  components: {Username},
  props: {
    data: {
      type: Object,
      required: true,
    }
  },
  data() {
    return {
      typesToColors: {
        "failure": "danger",
        "lazy_loading": "warning",
        "report": "secondary",
        "review": "primary"
      },

      typesToIcons: {
        "failure": "fa-times",
        "lazy_loading": "fa-signal",
        "report": "fa-exclamation-circle",
        "review": "fa-comments"
      },


    }
  }
}
</script>

<style scoped>

</style>