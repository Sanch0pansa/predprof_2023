<template>
  <FormEl @handle="handle">
    <StarRating
        :label="`Ваша оценка:`"
        v-model="mark"
    ></StarRating>
    <TxtArea
        :name="`message`"
        :label="`Сообщение:`"
        v-model="message"
        v-model:errors="errorBag.message">
    </TxtArea>
    <br>
    <Btn>Оставить отзыв</Btn>
    <ErrorBag v-model:errors="errorBag.non_field_errors" v-model:success="errorBag.success"></ErrorBag>
  </FormEl>
</template>

<script>
import TxtArea from "@/components/UI/TxtArea.vue";
import {mapActions} from "vuex";
import {errorBagFill} from "@/components/forms/errorBag";
import FormEl from "@/components/UI/FormEl.vue";


export default {
  name: "CreatingReviewForm",
  components: {FormEl, TxtArea},
  props: {
    id: {
      required: true,
      type: Number
    }
  },
  data() {
    return {
      message: "",
      mark: 5,
      errorBag: {
        mark: [],
        message: [],
        non_field_errors: [],
        success: "",
      }
    }
  },

  methods: {

    ...mapActions({
      createReview: "reviews/createReview"
    }),

    async handle() {
      let res = await this.createReview({
        id: this.id,
        message: this.message,
        mark: this.mark
      });

      errorBagFill(this.errorBag, res);
    }
  }
}
</script>

<style scoped>

</style>