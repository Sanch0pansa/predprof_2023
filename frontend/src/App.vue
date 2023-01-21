<script>
import { RouterLink, RouterView } from 'vue-router'
import PageHeader from "@/components/page/PageHeader.vue";
import PageFooter from "@/components/page/PageFooter.vue";
import PageTable from "@/components/page/PageTable.vue";
import PageWelcomeSection from "@/components/page/PageWelcomeSection.vue";
import PagesList from "@/components/items/PagesList.vue";
import PageSiteStatistics from "@/components/page/PageSiteStatistics.vue";

export default {
  components: {PageHeader, PageFooter, PageTable, PageWelcomeSection, PagesList, PageSiteStatistics},

}
</script>

<template>
<div class="wrapper">
  <PageHeader></PageHeader>
  <div class="container main pb-5">

    <RouterView></RouterView>

  </div>
  <PageFooter></PageFooter>
</div>
</template>

<style scoped>
</style>
