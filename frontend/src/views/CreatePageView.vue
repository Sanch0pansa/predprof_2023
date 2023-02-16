<template>
  <div class="row pt-5">
    <PageBreadcrumbs :links-names="['create_page']"></PageBreadcrumbs>
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
import PageBreadcrumbs from "@/components/page/PageBreadcrumbs.vue";

export default {
  name: "CreatePageView.vue",
  components: {PageBreadcrumbs, CreatingPageForm}
}
</script>

<style scoped>

</style>