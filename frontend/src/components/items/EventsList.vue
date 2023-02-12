<template>
  <ul class="list-group list-group-flush">
    <EventsListItem :data="event" v-for="event in events"></EventsListItem>
  </ul>
</template>

<script>
import EventsListItem from "@/components/items/EventsListItem.vue";

export default {
  name: "EventsList",
  components: {EventsListItem},
  props: {
    events: {
      required: true,
      type: Array,
    }
  }
}
</script>

<style scoped>

</style>