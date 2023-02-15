<template>
  <FormEl @handle="handle">
    <Inp
        :name="`name`"
        :label="`Название ресурса:`"
        :type="`text`"
        v-model="name"
        v-model:errors="errorBag.name">
    </Inp>
    <br>
    <TxtArea
        :name="`description`"
        :label="`Описание ресурса:`"
        v-model="description"
        v-model:errors="errorBag.description">
    </TxtArea>
    <br>
    <Inp
        :name="`url`"
        :label="`Ссылка на ресурс (вместе с протоколом):`"
        :type="`text`"
        v-model="url"
        v-model:errors="errorBag.url">
    </Inp>
    <br>
    <Btn>Сохранить</Btn>
    <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
  </FormEl>
</template>

<script>
import FormEl from "@/components/UI/FormEl.vue";
import TxtArea from "@/components/UI/TxtArea.vue";
import {mapActions} from "vuex";
import {errorBagFill} from "@/components/forms/errorBag";

export default {
  name: "CreatingPageForm",
  components: {FormEl, TxtArea},
  data() {
    return {
      name: "",
      description: "",
      url: "",
      errorBag: {
        name: [],
        description: [],
        url: [],
        non_field_errors: [],
        success: "",
      }
    }
  },

  methods: {

    ...mapActions({
      "createPage": "pages/createPage"
    }),

    async handle() {
      let urlRegExp = /^(https?):\/\/([А-Яа-яa-zA-Z0-9.-]+(:[А-Яа-яa-zA-Z0-9.&%$-]+)*@)*((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])){3}|([А-Яа-яa-zA-Z0-9-]+\.)*[А-Яа-яa-zA-Z0-9-]+\.(com|edu|gov|int|mil|net|org|biz|arpa|info|name|pro|aero|coop|museum|онлайн|москва|[А-Яа-яa-zA-Z]{2}))(:[0-9]+)*(\/($|[А-Яа-яa-zA-Z0-9.,?'\\+&%$#=~_-]+))*$/;
      let urlIsValid = urlRegExp.test(this.url);

      if (!urlIsValid) {
        let invalidUrlErrorText = "Ссылка не валидна";
        if (!this.errorBag.url.includes(invalidUrlErrorText)) {
          this.errorBag.url.push(invalidUrlErrorText);
        }

        return null;
      }

      let res = await this.createPage({
        name: this.name,
        description: this.description,
        url: this.url
      });

      errorBagFill(this.errorBag, res);

      if (res.success) {
        setTimeout(() => {
          this.$router.replace({ name: 'account' })
        }, 1500);
      }
    }
  }
}
</script>

<style scoped>

</style>