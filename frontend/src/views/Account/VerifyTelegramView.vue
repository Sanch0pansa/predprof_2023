<template>
  <div class="row pt-5 text-center">
    <div class="col-md-4"></div>
    <div class="col-md-4">
      <h2 class="mb-5">Авторизация</h2>
      <Block>
        <p class="text-muted">Отправьте этот код нашему<br><a href="https://t.me/site_ping_bot" target="_blank">телеграм-боту</a></p>
        <div class="alert alert-primary my-4">
          <h1 style="letter-spacing: 2px">{{ code }}</h1>
        </div>
        <Btn @click="fetchCode" v-if="can_repeat">Сгенерировать новый код</Btn>
        <Btn v-else disabled="disabled">Другой код через {{ String(remain_time) }} сек.</Btn>
      </Block>
    </div>
  </div>

</template>

<script>
import PageSection from "@/components/UI/Section.vue";
import Block from "@/components/UI/Block.vue";
import {mapActions} from "vuex";

export default {
  name: "VerifyTelegram",
  components: {Block, PageSection},
  methods: {
    ...mapActions({
      generateTelegramCode: "telegram/generateTelegramCode"
    }),

    async fetchCode() {
      let res = await this.generateTelegramCode();

      if (res.code) {
        this.code = res.code;
      }

      if (!res.success) {
        this.can_repeat = false;
        this.remain_time = res.remain_time;

        this.timer();
      }


    },

    async timer() {
      console.log("timed");
      if (this.remain_time > 0) {
        setTimeout(() => {
          this.timer();
        }, 1000);
        this.remain_time -= 1;
      } else {
        this.can_repeat = true;
      }
    }
  },

  data() {
    return {
      code: 0,
      can_repeat: true,
      remain_time: 0,
    }
  },

  async mounted() {
    await this.fetchCode();
  }
}
</script>

<style scoped>

</style>