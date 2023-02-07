<template>
  <div class="row pt-5">
    <div class="col-12">
      <h1>Добавление ресурса</h1>
      <Block class="mt-4">
        <CreatingPageForm>

        </CreatingPageForm>
      </Block>
    </div>
  </div>
</template>

<script>
import CreatingPageForm from "@/components/forms/CreatingPageForm.vue";

export default {
  name: "CreatePageView.vue",
  components: {CreatingPageForm}
}
</script>

<style scoped>

</style>