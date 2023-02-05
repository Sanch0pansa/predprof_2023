<template>
  <FormEl @handle="handle">
    <TxtArea
        :name="`message`"
        :label="`Опишите подробности сбоя:`"
        v-model="message"
        v-model:errors="errorBag.message">
    </TxtArea>
    <br>
    <Inp
        :name="`added_at_date`"
        :label="`Укажите дату сбоя:`"
        :type="`date`"
        v-model="added_at_date"
        v-model:errors="errorBag.added_at">
    </Inp>
    <br>
    <Inp
      :name="`added_at_time`"
      :label="`Укажите время сбоя:`"
      :type="`time`"
      v-model="added_at_time"
      v-model:errors="errorBag.added_at">
    </Inp>
    <br>
    <Btn>Сообщить</Btn>
    <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
  </FormEl>
</template>

<script>
import TxtArea from "@/components/UI/TxtArea.vue";
import {mapActions} from "vuex";
import {errorBagFill} from "@/components/forms/errorBag";
import FormEl from "@/components/UI/FormEl.vue";

export default {
  name: "CreatingReportForm",
  components: {FormEl, TxtArea},
  props: {
    id: {
      required: true,
      type: Number
    }
  },
  data() {
    let date = new Date();
    let dateTime = (new Date(date.getTime() - (date.getTimezoneOffset() * 60000))).toISOString();
    return {
      message: "",
      added_at_date: dateTime.split('T')[0],
      added_at_time: dateTime.split('T')[1].slice(0, 5),
      errorBag: {
        added_at: [],
        message: [],
        non_field_errors: [],
        success: "",
      }
    }
  },

  methods: {

    ...mapActions({
      createReport: "reports/createReport"
    }),

    async handle() {
      let res = await this.createReport({
        id: this.id,
        message: this.message,
        added_at: this.added_at_date + "T" + this.added_at_time,
      });

      errorBagFill(this.errorBag, res);
    }
  }
}
</script>

<style scoped>

</style>