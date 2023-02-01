<template>
  <div class="d-flex flex-column gap-3">
    <!--  <PagesListItem v-for="obj in [0, 1, 2]" :status="obj" :href="`https://google.com`"></PagesListItem>-->
    <SubscriptionsListItem v-for="obj in pages" :status="obj.check_status" :href="{name: 'single_page', params: {id: obj.id}}" :name="obj.name"></SubscriptionsListItem>
  </div>
</template>

<script>
import SubscriptionsListItem from "@/components/items/SubscriptionsListItem.vue";

export default {
  components: {SubscriptionsListItem},
  name: "SubscriptionsList",
  props: {
    pages: {
      required: true,
      type: Array,
    }
  }
}
</script>

<style scoped>

</style>