<template>
  <div class="row pt-5 text-center">
    <div class="col-md-4"></div>
    <div class="col-md-4">
      <h2 class="mb-5">Привязка Telegram</h2>
      <Block v-if="$store.state.auth.user.telegram_id == null">
        <p class="text-muted">Отправьте этот код нашему<br><a href="https://t.me/site_ping_bot" target="_blank">телеграм-боту</a></p>
        <div class="alert alert-primary my-4 position-relative">
          <h1 style="letter-spacing: 2px">{{ code }}</h1>
          <i role="button" class="fs-5 text-primary fas fa-copy position-absolute" style="right: 10px; top: 10px;" @click="copyCode"></i>
        </div>
        <Btn @click="fetchCode" v-if="canRepeat">Сгенерировать новый код</Btn>
        <Btn v-else disabled="disabled">Другой код через {{ String(remainTime) }} сек.</Btn>
      </Block>
      <Block v-else>
        <div class="alert alert-success my-4 position-relative">
          <h3>Привязано</h3>
        </div>
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

  data() {
    return {
      code: 0,
      canRepeat: true,
      remainTime: 0,
      timerTimeout: null,
    }
  },

  methods: {
    ...mapActions({
      generateTelegramCode: "telegram/generateTelegramCode",
      getUserData: "auth/getUserData",
    }),

    copyCode() {
      navigator.clipboard.writeText(this.code)
    },

    async fetchCode() {
      if (this.$store.state.auth.user.telegram_id != null) {
        if (this.timerTimeout) {
          clearTimeout(this.timerTimeout);
        }
        setTimeout(() => {
          this.$router.replace({name: "acccount"});
        }, 2000);
        return false;
      }
      let res = await this.generateTelegramCode();

      if (res.code) {
        this.code = res.code;

        if (this.timerTimeout) {
          clearTimeout(this.timerTimeout);
        }

        this.canRepeat = false;
        this.remainTime = res.remain_time;

        await this.timer();
      }
    },

    async timer() {
      if (this.remainTime > 0) {
        this.timerTimeout = setTimeout(async () => {
          await this.timer();
        }, 1000);
        this.remainTime -= 1;

        await this.getUserData();

        if (this.$store.state.auth.user.telegram_id != null) {
          if (this.timerTimeout) {
            clearTimeout(this.timerTimeout);
          }
          setTimeout(() => {
            this.$router.replace({name: "home"});
          }, 1000);
        }

      } else {
        this.canRepeat = true;
      }
    }
  },

  async mounted() {
    await this.fetchCode();
  },

  async unmounted() {
    // При демонтировании компонента таймер останавливается
    if (this.timerTimeout) {
      clearTimeout(this.timerTimeout);
    }
  }
}
</script>

<style scoped>

</style>