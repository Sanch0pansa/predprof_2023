<template>
<div class="row pt-5">
  <div class="col-12">
    <h1>Модерация страниц</h1>
  </div>
  <div class="col-12 mt-5 d-flex flex-column gap-3">
    <ModerationPagesList :pages="pages" @action="sendPatchPageStatus"></ModerationPagesList>
  </div>
</div>
</template>

<script>

import Tabs from "@/components/UI/Tabs.vue";
import ModerationPagesList from "@/components/items/ModerationPagesList.vue";
import {mapActions} from "vuex";

export default {
  name: "ModerationPagesView",
  components: {ModerationPagesList, Tabs},
  data() {
    return {
      pages: {
        moderation: [

        ],
        rejected: [

        ]
      }
    }
  },
  methods: {
    ...mapActions({
      getModerationPages: "moderation/getModerationPages",
      getRejectedPages: "moderation/getRejectedPages",
      patchPageStatus: "moderation/patchPageStatus",
    }),
    async fetchPages() {
      this.pages.moderation = await this.getModerationPages();
      this.pages.rejected = await this.getRejectedPages();
    },

    async sendPatchPageStatus({id, action}) {
        let res = await this.patchPageStatus({
          id: id,
          action: action
        });

        if (res.success) {
          await this.fetchPages();
        }
    }
  },
  async mounted() {
    await this.fetchPages();
  }
}
</script>

<style scoped>

</style>