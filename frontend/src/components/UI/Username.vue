<template>
<b data-bs-toggle="modal" :data-bs-target="`#modal-for-${username}`" class="text-primary" role="button" @click="fetchUserData">{{ username }}</b>
  <Modal :id="`modal-for-${username}`" :title="username">
    <p class="text-muted">Информация о пользователе: </p>
    <p>
      Оставлено сообщений о сбоях: <b>{{reports}}</b><br>
      Оставлено отзывов: <b>{{ reviews }}</b><br>
      Отслеживает ресурсов: <b>{{ subscriptions }}</b><br>
      Зарегистрирован: <b>{{ joined }}</b>
    </p>
  </Modal>
</template>

<script>
import ModalBtn from "@/components/UI/ModalBtn.vue";
import {mapActions} from "vuex";

export default {
  name: "Username",
  components: {ModalBtn},
  props: {
    username: {
      required: true,
      type: String,
    },
    id: {
      required: true,
      type: Number
    }
  },
  data() {
    return {
      reviews: 0,
      reports: 0,
      joined: '23 янв 2022',
      subscriptions: 0,
    }
  },
  methods: {

    ...mapActions({
      getUserData: "user/getUserData"
    }),

    async fetchUserData() {
      let res = await this.getUserData({id: this.id});

      this.reviews = res.reviews;
      this.reports = res.reports;
      this.subscriptions = res.subscriptions;
      this.joined = (new Date(res.joined)).toLocaleString("ru", {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: "numeric",
        minute: "numeric",
        second: "numeric"
      });
    },
  }
}
</script>

<style scoped>

</style>