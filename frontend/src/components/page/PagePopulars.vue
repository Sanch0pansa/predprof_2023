<template>
  <PageSection :title="`Популярные ресурсы`">
    <PagesList :pages="pages"></PagesList>
  </PageSection>
</template>

<script>
import PagesList from "@/components/items/PagesList.vue";
import {mapState, mapGetters, mapActions, mapMutations} from 'vuex'

export default {
  name: "PagePopulars",
  components: {PagesList},
  data() {
    return {
      pages: []
    }
  },

  async mounted() {
    await this.fetchPopularPages();
  },

  methods: {
    ...mapActions({
      getPopularPages: 'pages/getPopularPages',
    }),

    async fetchPopularPages() {
      this.pages = await this.getPopularPages();
    }
  }
}
</script>

<style scoped>

</style>