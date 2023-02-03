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
        :name="`added_at`"
        :label="`Укажите дату и время сбоя:`"
        :type="`date`"
        v-model="added_at"
        v-model:errors="errorBag.added_at">
    </Inp>
    <br>
    <Btn>Войти</Btn>
    <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
  </FormEl>
</template>

<script>
import TxtArea from "@/components/UI/TxtArea.vue";

export default {
  name: "CreatingReportForm",
  components: {TxtArea},
  data() {
    return {
      message: "",
      added_at: (new Date()).toISOString().split('T')[0],
      errorBag: {
        added_at: [],
        message: [],
        non_field_errors: [],
        success: "",
      }
    }
  },

  methods: {

  }
}
</script>

<style scoped>

</style>